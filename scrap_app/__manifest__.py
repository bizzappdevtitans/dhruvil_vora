# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "Scrap app",
    "category": "Uncategorized",
    "version": "15.0.1.0.0",
    "summary": "Management of scrap",
    "author": "Odoo Community Association (OCA)",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "views/scrap_desktop_view.xml",
        "views/scrap_category_view.xml",
        "views/scrap_collection_view.xml",
        "views/scrap_selling_view.xml",
        "views/scrap_inventory_view.xml",
        "views/product_category_view.xml",
        "views/product_product_view.xml",
        "views/scrap_items_views.xml",
        "views/res_config_settings_views.xml",
        "views/scrapapp_menu.xml",
    ],
    "demo": [
        "data/desktop_data.xml",
        "data/scrap_sequence.xml",
        "data/system_parameters.xml",
    ],
    "application": True,
    "license": "LGPL-3",
    "website": "https://github.com/OCAoca/",
}
