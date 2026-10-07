import gi

gi.require_version("Gio", "2.0")

from gi.repository import Gio


PTYXIS_SCHEMA = "org.gnome.Ptyxis"
PROFILE_SCHEMA = "org.gnome.Ptyxis.Profile"

PROFILE_PATH_TEMPLATE = (
    "/org/gnome/Ptyxis/Profiles/{uuid}/"
)


def schema_exists(schema_id):
    source = Gio.SettingsSchemaSource.get_default()

    if source is None:
        return False

    schema = source.lookup(
        schema_id,
        True,
    )

    return schema is not None


def get_default_profile_uuid():
    if not schema_exists(PTYXIS_SCHEMA):
        return None

    settings = Gio.Settings.new(
        PTYXIS_SCHEMA
    )

    uuid = settings.get_string(
        "default-profile-uuid"
    ).strip()

    if not uuid:
        return None

    return uuid


def get_profile_settings():
    if not schema_exists(PROFILE_SCHEMA):
        return None

    uuid = get_default_profile_uuid()

    if not uuid:
        return None

    path = PROFILE_PATH_TEMPLATE.format(
        uuid=uuid
    )

    try:
        settings = Gio.Settings.new_with_path(
            PROFILE_SCHEMA,
            path,
        )
    except Exception as error:
        print(
            "Warning: could not open "
            f"Ptyxis profile: {error}"
        )
        return None

    return settings


def apply_ptyxis_opacity(opacity):
    settings = get_profile_settings()

    if settings is None:
        # This is expected when developing on Mint
        # without Ptyxis installed.
        return False

    try:
        value = float(opacity)

        value = max(
            0.0,
            min(1.0, value),
        )

        settings.set_double(
            "opacity",
            value,
        )

        Gio.Settings.sync()

        return True

    except Exception as error:
        print(
            "Warning: could not set "
            f"Ptyxis opacity: {error}"
        )

        return False
