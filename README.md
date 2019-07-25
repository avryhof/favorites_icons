# Favorites Icons
```bash
pip install git+https://github.com/avryhof/favorites_icons.git
```

A simple plugin to generate all of your touch and favorites icons, as well as the needed tags to make them work.A

## settings.py
```python
ICON_SRC = '/path/to/a/big/file.png'

# Optional
# A list of numbers for icon sizes... they will all be generated and tagged.
ICON_SIZES = [16, 32, 57, 60, 64, 72, 76, 96, 114, 120, 144, 152, 180, 192, 256, 512]
```