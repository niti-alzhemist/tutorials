{
    "name": "Real Estate",
    "summary": "Test module",
    "version": "17.0.0.0.0",
    "license": "OEEL-1",
    "depends": ["base"],
    "application": True,
    "data": [
        # Security
        "security/res_groups.xml",
        "security/ir.model.access.csv",
        # View
        "views/estate_property_views.xml",
        "views/estate_menu.xml",
    ],
    "demo": ["demo/demo.xml"],
}
