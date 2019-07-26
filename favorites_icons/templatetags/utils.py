import os
import re

from PIL import Image
from django.conf import settings


def url_join(*args):
    os_path = os.path.join(*args)
    path_parts = re.split(r'/|\\', os_path)

    return "/".join(path_parts)


def generate_icons(**kwargs):
    overwrite = kwargs.get("overwrite", False)

    static_root = getattr(settings, "STATIC_ROOT", False)
    icon_path = os.path.join(static_root, "favicons")

    icon_source = getattr(settings, "ICON_SRC", False)
    icon_sizes = getattr(
        settings, "ICON_SIZES", [16, 32, 57, 60, 64, 72, 76, 96, 114, 120, 144, 152, 180, 192, 256, 512]
    )
    ico_sizes = [(16, 16), (32, 32), (48, 48), (64, 64)]

    if icon_source:
        if not os.path.exists(icon_path):
            os.makedirs(icon_path)

        img = Image.open(icon_source)

        ico_target = os.path.join(icon_path, "favicon.ico")
        if overwrite or not os.path.exists(ico_target):
            img.save(ico_target, sizes=ico_sizes)

        icon_sizes = sorted(icon_sizes, reverse=True)
        # Use the same image object, start with the largest size, and work our way down.
        for icon_size in icon_sizes:
            target_file = os.path.join(icon_path, "favicon-%ix%i.png" % (icon_size, icon_size))
            if overwrite or not os.path.exists(target_file):
                img.thumbnail((icon_size, icon_size), Image.ANTIALIAS)
                img.save(target_file, "PNG")
