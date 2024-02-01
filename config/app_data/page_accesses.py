permissions = [
    {
        'codename': 'management_read_only',
        'description': 'Can access /management pages',
    },
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
    'management': ['management_read_only', 'manage_restaurant', 'manage_menu', 'manage_order'],
    'management_read_only': ['management_read_only'],
    'chef': ['manage_order']
}

page_accesses = {
    'papapay.management': {
        'management-page': ['management_read_only'],
        'manage-restaurants': ['management_read_only', 'manage_restaurant'],
        'create-restaurant': ['manage_restaurant'],
        'update-restaurant': ['manage_restaurant'],
        'delete-restaurant-api': ['manage_restaurant'],
        'manage-menus': ['management_read_only', 'manage_menu'],
        'manage-orders': ['management_read_only', 'manage_order'],
    },
}
