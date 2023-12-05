from django.contrib.auth.management import create_permissions
from django.contrib.auth.models import Group, Permission
from .models import User


def populate_groups(apps, schema_editor):
    """
    This function is run in migrations/0002_initial_data.py as an initial
    data migration at project initialization. it sets up some basic model-level
    permissions for different groups when the project is initialised.

    Admin Group: Able to add new users, and edit non-admin users
    Member: Regular members of a given constellation. We explicitly grant them permissions
    to create new tags, because the autocomplete code requires this.
    """

    # Create user groups
    user_roles = ["admin", "member"]
    for name in user_roles:
        if not Group.objects.filter(name=name).exists():
            Group.objects.create(name=name)

    # Permissions have to be created before applying them
    for app_config in apps.get_app_configs():
        app_config.models_module = True
        create_permissions(app_config, verbosity=0)
        app_config.models_module = None

    # Assign model-level permissions to regular members
    member_group = Group.objects.get(name="member")

    member_perm_codes = [
        "add_tag",
        # 'change_tag',
        # 'delete_tag',
        # 'view_tag',
    ]

    for perm_code in member_perm_codes:
        perm = Permission.objects.get(codename=perm_code)
        member_group.permissions.add(perm)

    for user in User.objects.all():
        member_group.user_set.add(user)
        user.save()

    member_group.save()

    # Then assign default permissions to admins
    admin_group = Group.objects.get(name="admin")
    admin_perm_codes = [
        "add_emailaddress",
        "change_emailaddress",
        "delete_emailaddress",
        "view_emailaddress",
        "change_group",
        "view_group",
    ]

    for perm_code in admin_perm_codes:
        perm = Permission.objects.get(codename=perm_code)
        admin_group.permissions.add(perm)
