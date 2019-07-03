{
    "name": "Denker - Stock Reports Fields",
    "version": "11.0.1",
    'author': 'Servicios Corporativos Denker - BC',
    'website': 'www.grupodenker.com',
    'license': 'AGPL-3',
    "category": "Accounting",
    'summary': 'Módulo para agregar campos para los reportes desde Spreadsheets.',
    "description": """  Módulo para agregar campos para los reportes desde Spreadsheets.""",
    'depends': ['stock', 'dnk_sale_theoretical_cost'],
    'data': [
        'views/stock_move_line_views.xml',
        'views/stock_move_views.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
}
