permissions = [
    {
        'codename': 'manage_restaurant',
        'description': 'Can add/change/delete/view restaurants',
    },
    {
        'codename': 'manage_menu',
        'description': 'Can add/change/delete/view menus, menu items, item categories, ingredients, allergenes',
    },
    {
        'codename': 'manage_order',
        'description': 'Can add/change/delete/view orders',
    }
]

groups = {
    'management': ['manage_restaurant', 'manage_menu', 'manage_order'],
    'chef': ['manage_order']
}

page_accesses = [
    {
        'app_name': 'papapay.restaurant',
        'url_name': 'manage-restaurants',
        'permissions': ['manage_restaurant']
    }
]
