import os

ADMIN_PASSWORD = os.environ.get('ENV_ADMIN_PASSWORD', '1234')
STAFF_PASSWORD = os.environ.get('ENV_STAFF_PASSWORD', '1234')

users = [
    {
        "username": "admin", 
        "password": ADMIN_PASSWORD,
        "is_superuser": True,
        "is_staff": True
    },
    {
        "username": "samir", 
        "password": ADMIN_PASSWORD,
        "is_superuser": False,
        "is_staff": False
    },
    {
        "username": "yesid", 
        "password": STAFF_PASSWORD,
        "is_superuser": True,
        "is_staff": True
    },
    {
        "username": "mariacam", 
        "password": STAFF_PASSWORD,
        "is_superuser": False,
        "is_staff": True
    },
]
