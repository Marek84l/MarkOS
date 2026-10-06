#!/usr/bin/env python3

import configparser
from pathlib import Path

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Adw, Gtk, Gio


APP_ID = "io.markos.Appearance"

SYSTEM_ROOT = Path("/usr/share/markos")
SYSTEM_WALLPAPER_DIR = Path("/usr/share/backgrounds/markos")
SYSTEM_PRESET_DIR = SYSTEM_ROOT / "appearance"

# Development paths when running directly from the MarkOS repository.
DEV_ROOT = Path(__file__).resolve().parents[3]
DEV_WALLPAPER_DIR = (
    DEV_ROOT / "usr" / "share" / "backgrounds" / "markos"
)
DEV_PRESET_DIR = (
    DEV_ROOT / "usr" / "share" / "markos" / "appearance"
)


def get_preset_dir():
    if SYSTEM_PRESET_DIR.exists():
        return SYSTEM_PRESET_DIR

    return DEV_PRESET_DIR


def wallpaper_path(filename):
    system_path = SYSTEM_WALLPAPER_DIR / filename

    if system_path.exists():
        return system_path

    dev_path = DEV_WALLPAPER_DIR / filename

    if dev_path.exists():
        return dev_path

    print(f"Warning: wallpaper not found: {filename}")
    return dev_path


def file_uri(path):
    return Path(path).resolve().as_uri()


def load_presets():
    presets = []
    preset_dir = get_preset_dir()

    for path in sorted(preset_dir.glob("*.conf")):
        config = configparser.ConfigParser()
        config.read(path)

        if "MarkOS Appearance" not in config:
            continue

        section = config["MarkOS Appearance"]

        try:
            preset = {
                "id": path.stem,
                "name": section["Name"],
                "wallpaper": section["Wallpaper"],
                "scheme": section["ColorScheme"],
                "accent": section["AccentColor"],
                "icon_theme": section["IconTheme"],
                "terminal_palette": section.get(
                    "TerminalPalette",
                    path.stem,
                ),
                "terminal_opacity": section.getfloat(
                    "TerminalOpacity",
                    fallback=1.0,
                ),
                "starship_palette": section.get(
                    "StarshipPalette",
                    path.stem,
                ),
                "fastfetch_palette": section.get(
                    "FastfetchPalette",
                    path.stem,
                ),
            }

        except (KeyError, ValueError) as error:
            print(
                f"Warning: invalid preset {path.name}: {error}"
            )
            continue

        presets.append(preset)

    return presets


class MarkOSAppearance(Adw.Application):
    def __init__(self):
        super().__init__(application_id=APP_ID)

        self.presets = load_presets()
        self.preset_buttons = {}

        self.interface_settings = Gio.Settings.new(
            "org.gnome.desktop.interface"
        )

        self.background_settings = Gio.Settings.new(
            "org.gnome.desktop.background"
        )

        self.connect("activate", self.on_activate)

    def has_setting(self, settings, key):
        schema = settings.props.settings_schema
        return schema.has_key(key)

    def apply_preset(self, preset):
        path = wallpaper_path(
            preset["wallpaper"]
        )
        uri = file_uri(path)

        # Wallpaper
        self.background_settings.set_string(
            "picture-uri",
            uri,
        )

        self.background_settings.set_string(
            "picture-uri-dark",
            uri,
        )

        self.background_settings.set_string(
            "picture-options",
            "zoom",
        )

        # Dark / light appearance
        if self.has_setting(
            self.interface_settings,
            "color-scheme",
        ):
            self.interface_settings.set_string(
                "color-scheme",
                preset["scheme"],
            )

        # GNOME accent colour.
        # Mint may not expose this key, so development testing remains safe.
        if self.has_setting(
            self.interface_settings,
            "accent-color",
        ):
            self.interface_settings.set_string(
                "accent-color",
                preset["accent"],
            )

        # MarkOS icon theme
        if self.has_setting(
            self.interface_settings,
            "icon-theme",
        ):
            self.interface_settings.set_string(
                "icon-theme",
                preset["icon_theme"],
            )

        self.refresh_active_state()

    def current_wallpaper(self):
        uri = self.background_settings.get_string(
            "picture-uri"
        )

        if uri.startswith("file://"):
            return Path(uri[7:]).name

        return ""

    def refresh_active_state(self):
        current = self.current_wallpaper()

        for preset in self.presets:
            button = self.preset_buttons.get(
                preset["id"]
            )

            if button is None:
                continue

            if current == preset["wallpaper"]:
                button.set_label("✓ Active")
                button.add_css_class(
                    "suggested-action"
                )
            else:
                button.set_label("Apply")
                button.remove_css_class(
                    "suggested-action"
                )

    def create_preset_card(self, preset):
        card = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=12,
        )

        card.add_css_class("card")
        card.set_margin_top(4)
        card.set_margin_bottom(4)
        card.set_margin_start(4)
        card.set_margin_end(4)

        picture = Gtk.Picture.new_for_filename(
            str(
                wallpaper_path(
                    preset["wallpaper"]
                )
            )
        )

        picture.set_content_fit(
            Gtk.ContentFit.COVER
        )
        picture.set_size_request(-1, 135)
        picture.set_hexpand(True)
        picture.set_can_shrink(True)

        info_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=6,
        )

        info_box.set_margin_start(16)
        info_box.set_margin_end(16)

        name_label = Gtk.Label()
        name_label.set_markup(
            f"<span size='large' weight='bold'>"
            f"{preset['name']}"
            f"</span>"
        )
        name_label.set_xalign(0)

        mode = (
            "Dark"
            if preset["scheme"] == "prefer-dark"
            else "Light"
        )

        description = (
            f"{mode} • {preset['accent'].title()}"
        )

        description_label = Gtk.Label(
            label=description
        )
        description_label.set_xalign(0)
        description_label.add_css_class(
            "dim-label"
        )

        button = Gtk.Button(
            label="Apply"
        )

        button.set_margin_start(16)
        button.set_margin_end(16)
        button.set_margin_bottom(16)

        button.connect(
            "clicked",
            lambda _button, p=preset:
                self.apply_preset(p),
        )

        self.preset_buttons[
            preset["id"]
        ] = button

        info_box.append(name_label)
        info_box.append(description_label)

        card.append(picture)
        card.append(info_box)
        card.append(button)

        return card

    def on_activate(self, app):
        window = Adw.ApplicationWindow(
            application=app
        )

        window.set_title(
            "MarkOS Appearance"
        )
        window.set_default_size(
            780,
            700,
        )

        toolbar = Adw.ToolbarView()

        header = Adw.HeaderBar()
        toolbar.add_top_bar(header)

        clamp = Adw.Clamp()
        clamp.set_maximum_size(700)

        main_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=24,
        )

        main_box.set_margin_top(32)
        main_box.set_margin_bottom(32)
        main_box.set_margin_start(24)
        main_box.set_margin_end(24)

        title = Gtk.Label()
        title.set_markup(
            "<span size='xx-large' weight='bold'>"
            "Make MarkOS yours"
            "</span>"
        )
        title.set_xalign(0)

        subtitle = Gtk.Label(
            label=(
                "Choose a complete MarkOS "
                "appearance preset."
            )
        )
        subtitle.set_xalign(0)
        subtitle.add_css_class(
            "dim-label"
        )

        main_box.append(title)
        main_box.append(subtitle)

        grid = Gtk.Grid()
        grid.set_column_spacing(16)
        grid.set_row_spacing(16)
        grid.set_column_homogeneous(True)

        for index, preset in enumerate(
            self.presets
        ):
            card = self.create_preset_card(
                preset
            )

            row = index // 2
            column = index % 2

            grid.attach(
                card,
                column,
                row,
                1,
                1,
            )

        main_box.append(grid)

        clamp.set_child(main_box)
        toolbar.set_content(clamp)

        window.set_content(toolbar)

        self.refresh_active_state()

        window.present()


app = MarkOSAppearance()
app.run()
