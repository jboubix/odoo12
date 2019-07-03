# -*- coding: utf-8 -*-
{
    'name': "Denker - Product Category Restriction on Users",

    'summary': """
    User Allowed Product Categories Only.
    """,

    'description': """
        - This Module adds restriction on users for accessing products for any kind of operation.
        - User can not see the products if not allowed by the admin.
        - User can only see and operate on Allowed Products.
        - Restriction also applies to sales order, purchase order, stock transfer etc.
        - Admin can edit the user and add allowed produts to a specific user.
        - Note : This Restriction is Applied On Adminstrator.
    """,

    'author': "José Candelas",
    'website': "http://www.techspawn.com",

    'category': 'Product',
    'version': '12.0.1.0',

    'depends': ['base', 'stock', 'sale', 'product'],

    'data': [
        'security/security.xml',
        'views/user_view.xml',
    ],
}
