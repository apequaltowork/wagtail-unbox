# Give the default "Editors" group what the client actually edits: the team and
# testimonial snippets, and Studio settings.
#
# Done in a migration rather than by clicking in Settings -> Groups, so every
# copy of the site -- a colleague's laptop, staging, production -- ends up with
# the same permissions.

from django.contrib.auth.management import create_permissions
from django.db import migrations

GRANTS = [
    "add_teammember", "change_teammember", "delete_teammember",
    "add_testimonial", "change_testimonial", "delete_testimonial",
    "change_studiosettings",
]


def grant(apps, schema_editor):
    # Django creates Permission rows in a post_migrate signal -- after every
    # migration has run. On a fresh database they don't exist yet at this point,
    # so create them now.
    for app_config in apps.get_app_configs():
        app_config.models_module = True
        create_permissions(app_config, apps=apps, verbosity=0)
        app_config.models_module = None

    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    editors = Group.objects.filter(name="Editors").first()
    if editors is None:
        return  # a project that has deleted or renamed the group
    editors.permissions.add(
        *Permission.objects.filter(content_type__app_label="home", codename__in=GRANTS)
    )


def revoke(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    editors = Group.objects.filter(name="Editors").first()
    if editors:
        editors.permissions.remove(
            *Permission.objects.filter(content_type__app_label="home", codename__in=GRANTS)
        )


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0008_contactpage_formfield"),
        # The Editors group itself is created by this Wagtail migration.
        ("wagtailcore", "0002_initial_data"),
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [migrations.RunPython(grant, revoke)]
