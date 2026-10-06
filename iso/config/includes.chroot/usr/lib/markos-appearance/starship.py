from pathlib import Path
import re
import shutil


SYSTEM_TEMPLATE = Path(
    "/usr/share/markos/starship/starship.toml"
)

DEV_TEMPLATE = (
    Path(__file__).resolve().parents[3]
    / "usr"
    / "share"
    / "markos"
    / "starship"
    / "starship.toml"
)

USER_CONFIG = (
    Path.home()
    / ".config"
    / "starship.toml"
)


def template_path():
    if SYSTEM_TEMPLATE.exists():
        return SYSTEM_TEMPLATE

    return DEV_TEMPLATE


def apply_starship_palette(palette):
    source = template_path()

    if not source.exists():
        print(
            f"Warning: Starship template not found: {source}"
        )
        return False

    USER_CONFIG.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    text = source.read_text(
        encoding="utf-8"
    )

    text = re.sub(
        r'^palette\s*=\s*"[^"]+"',
        f'palette = "{palette}"',
        text,
        count=1,
        flags=re.MULTILINE,
    )

    USER_CONFIG.write_text(
        text,
        encoding="utf-8",
    )

    return True
