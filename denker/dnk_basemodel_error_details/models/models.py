# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2015 Deltatech All Rights Reserved
#                    Dorin Hongu <dhongu(@)gmail(.)com
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from odoo import api, fields, models, _, SUPERUSER_ID
from odoo.osv.query import Query
from odoo.models import BaseModel
from odoo.exceptions import AccessError
import logging

_logger = logging.getLogger(__name__)


class BaseModelExtend(models.AbstractModel):

    _name = 'basemodel.extend'

    @api.model_cr
    def _register_hook(self):

        @api.model
        def check_field_access_rights(self, operation, fields):
            """
            Check the user access rights on the given fields. This raises Access
            Denied if the user does not have the rights. Otherwise it returns the
            fields (as is if the fields is not falsy, or the readable/writable
            fields if fields is falsy).
            """
            if self._uid == SUPERUSER_ID:
                return fields or list(self._fields)

            def valid(fname):
                """ determine whether user has access to field ``fname`` """
                field = self._fields.get(fname)
                if field and field.groups:
                    return self.user_has_groups(field.groups)
                else:
                    return True

            if not fields:
                fields = [name for name in self._fields if valid(name)]
            else:
                invalid_fields = {name for name in fields if not valid(name)}
                if invalid_fields:
                    _logger.info('Access Denied by ACLs for operation: %s, uid: %s, model: %s, fields: %s',
                        operation, self._uid, self._name, ', '.join(invalid_fields))
                    # raise AccessError(_('The requested operation cannot be completed due to security restrictions. '
                    #                    'Please contact your system administrator.\n\n(Document type: %s, Operation: %s)') % \
                    #                  (self._description, operation))
                    # Modificación del mensaje de error: José Candelas
                    raise AccessError(_('The requested operation cannot be completed due to security restrictions. '
                                        'Please contact your system administrator.\n\n(Document type: %s, Operation: %s, Invalid fields: %s)') % \
                                      (self._description, operation, invalid_fields))

            return fields


        @api.multi
        def _read_from_database(self, field_names, inherited_field_names=[]):
            """ Read the given fields of the records in ``self`` from the database,
                and store them in cache. Access errors are also stored in cache.

                :param field_names: list of column names of model ``self``; all those
                    fields are guaranteed to be read
                :param inherited_field_names: list of column names from parent
                    models; some of those fields may not be read
            """
            if not self:
                return

            env = self.env
            cr, user, context = env.args

            # make a query object for selecting ids, and apply security rules to it
            param_ids = object()
            query = Query(['"%s"' % self._table], ['"%s".id IN %%s' % self._table], [param_ids])
            self._apply_ir_rules(query, 'read')

            # determine the fields that are stored as columns in tables; ignore 'id'
            fields_pre = [
                field
                for field in (self._fields[name] for name in field_names + inherited_field_names)
                if field.name != 'id'
                if field.base_field.store and field.base_field.column_type
                if not (field.inherited and callable(field.base_field.translate))
            ]

            # the query may involve several tables: we need fully-qualified names
            def qualify(field):
                col = field.name
                res = self._inherits_join_calc(self._table, field.name, query)
                if field.type == 'binary' and (context.get('bin_size') or context.get('bin_size_' + col)):
                    # PG 9.2 introduces conflicting pg_size_pretty(numeric) -> need ::cast
                    res = 'pg_size_pretty(length(%s)::bigint)' % res
                return '%s as "%s"' % (res, col)

            qual_names = [qualify(name) for name in [self._fields['id']] + fields_pre]

            # determine the actual query to execute
            from_clause, where_clause, params = query.get_sql()
            query_str = "SELECT %s FROM %s WHERE %s" % (",".join(qual_names), from_clause, where_clause)

            result = []
            param_pos = params.index(param_ids)
            for sub_ids in cr.split_for_in_conditions(self.ids):
                params[param_pos] = tuple(sub_ids)
                cr.execute(query_str, params)
                result.extend(cr.dictfetchall())

            ids = [vals['id'] for vals in result]
            fetched = self.browse(ids)

            if ids:
                # translate the fields if necessary
                if context.get('lang'):
                    for field in fields_pre:
                        if not field.inherited and callable(field.translate):
                            name = field.name
                            translate = field.get_trans_func(fetched)
                            for vals in result:
                                vals[name] = translate(vals['id'], vals[name])

                # store result in cache
                for vals in result:
                    record = self.browse(vals.pop('id'), self._prefetch)
                    record._cache.update(record._convert_to_cache(vals, validate=False))

                # determine the fields that must be processed now;
                # for the sake of simplicity, we ignore inherited fields
                for name in field_names:
                    field = self._fields[name]
                    if not field.column_type:
                        field.read(fetched)

            # Warn about deprecated fields now that fields_pre and fields_post are computed
            for name in field_names:
                field = self._fields[name]
                if field.deprecated:
                    _logger.warning('Field %s is deprecated: %s', field, field.deprecated)

            # store failed values in cache for the records that could not be read
            missing = self - fetched
            if missing:
                extras = fetched - self
                if extras:
                    raise AccessError(
                        _("Database fetch misses ids ({}) and has extra ids ({}), may be caused by a type incoherence in a previous request").format(
                            missing._ids, extras._ids,
                        ))
                # mark non-existing records in missing
                forbidden = missing.exists()
                if forbidden:
                    _logger.info(
                        _('The requested operation cannot be completed due to record rules: Document type: %s, Operation: %s, Records: %s, User: %s') % \
                        (self._name, 'read', ','.join([str(r.id) for r in self][:6]), self._uid))
                    # store an access error exception in existing records
                    exc = AccessError(
                        # _('The requested operation cannot be completed due to security restrictions. Please contact your system administrator.\n\n(Document type: %s, Operation: %s)') % \
                        # (self._name, 'read')
                        # Modificación del mensaje de error: José Candelas
                        _('The requested operation cannot be completed due to security restrictions. Please contact your system administrator.\n\n(Document type: %s, Operation: %s, Forbidden: %s)') % \
                        (self._name, 'read', forbidden)
                    )
                    self.env.cache.set_failed(forbidden, self._fields.values(), exc)


        @api.multi
        def _check_record_rules_result_count(self, result_ids, operation):
            """ Verify the returned rows after applying record rules matches the
                length of ``self``, and raise an appropriate exception if it does not.
            """
            ids, result_ids = set(self.ids), set(result_ids)
            missing_ids = ids - result_ids
            if missing_ids:
                # Attempt to distinguish record rule restriction vs deleted records,
                # to provide a more specific error message
                self._cr.execute('SELECT id FROM %s WHERE id IN %%s' % self._table, (tuple(missing_ids),))
                forbidden_ids = [x[0] for x in self._cr.fetchall()]
                if forbidden_ids:
                    # the missing ids are (at least partially) hidden by access rules
                    if self._uid == SUPERUSER_ID:
                        return
                    _logger.info('Access Denied by record rules for operation: %s on record ids: %r, uid: %s, model: %s', operation, forbidden_ids, self._uid, self._name)
                    # raise AccessError(_('The requested operation cannot be completed due to security restrictions. Please contact your system administrator.\n\n(Document type: %s, Operation: %s)') % \
                    #                    (self._description, operation))
                    # Modificación del mensaje de error: José Candelas
                    raise AccessError(_('The requested operation cannot be completed due to security restrictions. Please contact your system administrator.\n\n(Document type: %s, Operation: %s, Forbidden IDs: %s)') % \
                                        (self._description, operation, forbidden_ids))
                else:
                    # If we get here, the missing_ids are not in the database
                    if operation in ('read','unlink'):
                        # No need to warn about deleting an already deleted record.
                        # And no error when reading a record that was deleted, to prevent spurious
                        # errors for non-transactional search/read sequences coming from clients
                        return
                    _logger.info('Failed operation on deleted record(s): %s, uid: %s, model: %s', operation, self._uid, self._name)
                    raise MissingError(_('Missing document(s)') + ':' + _('One of the documents you are trying to access has been deleted, please try again after refreshing.'))

        models.AbstractModel.check_field_access_rights = check_field_access_rights
        models.AbstractModel._read_from_database = _read_from_database
        models.AbstractModel._check_record_rules_result_count = _check_record_rules_result_count
        return super(BaseModelExtend, self)._register_hook()
