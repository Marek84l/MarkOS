import json
from pathlib import Path


SYSTEM_TEMPLATE = Path(
    "/usr/share/markos/fastfetch/config.jsonc"
)

DEV_TEMPLATE = (
    Path(__file__).resolve().parents[3]
    / "usr"
    / "share"
    / "markos"
    / "fastfetch"
    / "config.jsonc"
)

USER_CONFIG = (
    Path.home()
    / ".config"
    / "fastfetch"
    / "config.jsonc"
)


PALETTES = {
    "cosmic": {
        "primary": "magenta",
        "secondary": "blue",
        "tertiary": "cyan",
    },
    "midnight": {
        "primary": "blue",
        "secondary": "cyan",
        "tertiary": "blue",
    },
    "aurora": {
        "primary": "green",
        "secondary": "cyan",
        "tertiary": "green",
    },
    "dawn": {
        "primary": "yellow",
        "secondary": "red",
        "tertiary": "magenta",
    },
}


def template_path():
    if SYSTEM_TEMPLATE.exists():
        return SYSTEM_TEMPLATE

    return DEV_TEMPLATE


def apply_fastfetch_palette(palette):
    source = template_path()

    if not source.exists():
        print(
            f"Warning: Fastfetch template not found: {source}"
        )
        return False

    colours = PALETTES.get(palette)

    if colours is None:
        print(
            f"Warning: unknown Fastfetch palette: {palette}"
        )
        return False

    text = source.read_text(
        encoding="utf-8"
    )

    # JSONC used by MarkOS currently contains no comments that
    # interfere with standard JSON parsing.
    config = json.loads(text)

    colour_cycle = [
        colours["primary"],
        colours["primary"],
        colours["secondary"],
        colours["secondary"],
        colours["tertiary"],
        colours["tertiary"],
    ]

    index = 0

    for module in config.get("modules", []):
        if not isinstance(module, dict):
            continue

        if "keyColor" not in module:
            continue

        module["keyColor"] = colour_cycle[
            index % len(colour_cycle)
        ]

        index += 1

    USER_CONFIG.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    USER_CONFIG.write_text(
        json.dumps(
            config,
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )

    return True
