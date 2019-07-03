{
    "name": "Denker - Add Untaxed USD Amount to Invoice",
    "version": "12.0.1",
    'author': 'Servicios Corporativos Denker - BC',
    'website': 'www.grupodenker.com',
    'license': 'AGPL-3',
    'summary': 'Se agrega el campo de monto en USD a Facturas y Pagos',
    "category": "Account Invoice",
    "description": """ This module add Untaxed USD amount in Account Invoice,
                       Account Invoice Line and Account Payment .""",
    'depends': ['account'],
    'data': [
        'views/account_invoice.xml',
        'views/account_payment.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
}
