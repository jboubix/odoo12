# © 2016 OdooMRP team
# © 2016 AvanzOSC
# © 2016 Serv. Tecnol. Avanzados - Pedro M. Baeza
# © 2016 Eficent Business and IT Consulting Services, S.L.
# Copyright 2017 Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
# -*- coding: utf-8 -*-
{
    'name': "Denker - Secondary Company Logo",

    'summary': """
        Agrega otro campo de logo en "compañías" para poderlo agregar en el encabezado de los documentos externos como cotizaciones y facturas.
        """,

    'description': """
        Agrega otro campo de logo en "compañías" para poderlo agregar en el encabezado de los documentos externos como cotizaciones y facturas.

        Agregar al encabezado el siguiente hypertexto:
        <img t-if="company.logo2" t-att-src="'data:image/png;base64,%s' % to_text(company.logo2)" class="pull-right"/>

        Si es "Background", reemplazar el encabezado:
        <div class="header o_boxed_header">
            <div class="row mb8">
                <div class="col-xs-6">
                    <img t-if="company.logo" t-att-src="'data:image/png;base64,%s' % to_text(company.logo)"/>
                </div>
                <div class="col-xs-6 text-right mb4">
                    <h4 class="mt0" t-field="company.report_header"/>
                    <div name="company_address" class="mb4">
                        <span class="company_address" t-field="company.partner_id" t-field-options="{&quot;widget&quot;: &quot;contact&quot;, &quot;fields&quot;: [&quot;address&quot;, &quot;name&quot;], &quot;no_marker&quot;: true}"/>
                    </div>
                </div>
            </div>
        </div>
        por:
        <div class="header o_background_header">
            <table cellpadding="0" cellspacing="0" border="0">
                <tr>
                    <td>
                        <img t-if="company.logo" t-att-src="'data:image/png;base64,%s' % to_text(company.logo)"/>
                    </td>
                    <td>
                        <div class="pull-left company_address">
                            <div>
                                <strong t-field="company.partner_id.name"/>
                            </div>
                            <span t-field="company.partner_id" t-field-options="{&quot;widget&quot;: &quot;contact&quot;, &quot;fields&quot;: [&quot;address&quot;], &quot;no_marker&quot;: true}"/>
                            <h2 class="mt0 text-right" t-field="company.report_header"/>
                        </div>
                    </td>
                    <td>
                        <img t-if="company.logo2" t-att-src="'data:image/png;base64,%s' % to_text(company.logo2)"/>
                    </td>
                </tr>
            </table>
        </div>
    """,

    'author': "José Candelas",
    'website': "http://www.grupodenker.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Sales',
    'version': '12.0.1.0',

    # any module necessary for this one to work correctly
    'depends': ['sale'],

    # always loaded
    'data': [
        'views/company_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}
