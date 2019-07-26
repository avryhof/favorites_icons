import json
import os
import re

from PIL import Image
from django.conf import settings
from django.contrib.sites.models import Site


def url_join(*args):
    os_path = os.path.join(*args)
    path_parts = re.split(r"/|\\", os_path)

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


def generate_manifest():
    static_root = getattr(settings, "STATIC_ROOT", False)
    static_url = getattr(settings, "STATIC_URL", False)

    icon_path = os.path.join(static_root, "favicons")
    icon_url = os.path.join(static_url, "favicons")

    target_file = os.path.join(icon_path, "manifest.json")

    icon_sizes = getattr(
        settings, "ICON_SIZES", [16, 32, 57, 60, 64, 72, 76, 96, 114, 120, 144, 152, 180, 192, 256, 512]
    )

    site_name = False
    current_site = False

    if hasattr(settings, "SITE_ID"):
        current_site = Site.objects.get_current()

    if hasattr(settings, "SITE_NAME"):
        site_name = getattr(settings, "SITE_NAME")

    elif not site_name and isinstance(current_site, Site):
        site_name = current_site.name

    if not site_name:
        site_name = "My app"

    manifest = {"name": site_name, "icons": []}

    density_factor = 48
    for icon_size in icon_sizes:
        icon_url = url_join(icon_url, "favicon-%ix%i.png" % (icon_size, icon_size))

        manifest["icons"].append(
            {
                "src": icon_url,
                "sizes": "%ix%i" % (icon_size, icon_size),
                "type": "image/png",
                "density": str(icon_size / density_factor),
            }
        )

    with open(target_file, "w") as manifest_file:
        json.dump(manifest, manifest_file)
        manifest_file.close()
