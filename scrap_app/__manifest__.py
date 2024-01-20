# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "Scrap_app",
    "category": "Uncategorized",
    "version": "15.0.1.0.0",
    "summary": "Management of scrap",
    "description": """
This module gives you a quick view of your scrap collection and management.
""",
    "author": "Scrap",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "views/scrap_desktop_view.xml",
        "views/scrap_category_view.xml",
        "views/scrap_collection_view.xml",
        "views/scrap_selling_view.xml",
        "views/scrap_menu.xml",
    ],
    "application": True,
    "license": "LGPL-3",
    # "website": "https://www.bizzappdev.com/",
}
