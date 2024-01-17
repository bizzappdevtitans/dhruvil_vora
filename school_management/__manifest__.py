# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "school_management",
    "category": "Uncategorized",
    "version": "15.0.1.0.0",
    "summary": "Management of school",
    "description": """
This module gives you a quick view of your contacts directory, accessible from your
home page. You can track your vendors, customers and other contacts.
""",
    "author": "School",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "views/school_details_views.xml",
        # "views/school_management_views.xml",
    ],
    "application": True,
    "license": "LGPL-3",
    # "website": "https://www.bizzappdev.com/",
}
