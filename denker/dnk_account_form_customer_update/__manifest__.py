{
    "name": "Denker - Update Customer Fields on Invoice",
    "version": "12.0.1",
    'author': 'Servicios Corporativos Denker - BC',
    'website': 'www.grupodenker.com',
    'license': 'AGPL-3',
    'summary': 'Actualizar los campos de CDFI del cliente al crear una factura.',
    "category": "Account Invoice",
    "description": """ Actualizar los campos de CDFI del cliente al crear una factura.""",
    'depends': ['account', 'sale'],
    'data': [
        'views/res_partner.xml',
        #'views/account_payment.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
}
