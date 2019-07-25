"""
@copyright Amos Vryhof

"""
import os

from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

from .utils import generate_icons

register = template.Library()


@register.simple_tag
def touch_icons():
    generate_icons()

    static_root = getattr(settings, "STATIC_URL", False)
    icon_path = os.path.join(static_root, "favicons")

    icon_sizes = getattr(
        settings, "ICON_SIZES", [16, 32, 57, 60, 64, 72, 76, 96, 114, 120, 144, 152, 180, 192, 256, 512]
    )

    icons = []
    for icon_size in icon_sizes:
        icon_url = os.path.join(icon_path, "favicon-%ix%i.png" % (icon_size, icon_size))

        icons.append('<link rel="apple-touch-icon" sizes="%ix%i" href="%s">' % (icon_size, icon_size, icon_url))
        icons.append('<link rel="icon" type="image/png" sizes="%ix%i"  href="%s">' % (icon_size, icon_size, icon_url))

    icons.append(
        '<meta name="msapplication-TileImage" content="%s">' % os.path.join(icon_path, "favicon-%ix%i.png" % (144, 144))
    )

    favicon_url = os.path.join(icon_path, "favicon.ico")
    icons.append('<link rel="shortcut icon" href="%s" type="image/x-icon">' % favicon_url)
    icons.append('<link rel="icon" href="%s" type="image/x-icon">' % favicon_url)

    return mark_safe("\n".join(icons))
