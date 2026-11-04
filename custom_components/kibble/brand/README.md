# Kibble brand assets

An original geometric pet paw and food bowl icon drawn by
`scripts/generate_brand.py` on a dark navy rounded square, with a matching gold
`Kibble` wordmark for the landscape logo. No third-party artwork is used.

| File | Size | Purpose |
| --- | --- | --- |
| `icon.png` | 256 × 256 | Home Assistant and HACS icon |
| `icon@2x.png` | 512 × 512 | High-resolution icon |
| `logo.png` | 894 × 256 | Landscape integration logo; README artwork |
| `logo@2x.png` | 1788 × 512 | High-resolution landscape logo |

All images are RGBA PNGs with transparent outer corners and backgrounds. These
sizes follow the [HA brand image guidelines](https://contributors.home-assistant.io/core/integrations/brands/).
Home Assistant 2026.3 and later serves these assets from the integration's local
`brand/` directory. The gold wordmark works against light and dark backgrounds,
so separate dark variants are not required.

## Source and permission

The icon is drawn from geometric primitives in this repository's
`scripts/generate_brand.py` and is covered by the repository's MIT license
(Copyright (c) 2026 eigger). The wordmark is rendered with Pillow's bundled
Aileron Regular via
[`ImageFont.load_default`](https://pillow.readthedocs.io/en/stable/reference/ImageFont.html#PIL.ImageFont.load_default).
[Aileron](https://dotcolon.net/font/aileron/) permits commercial use and is
released with no rights reserved. No font file is redistributed or loaded from
the system.

## Reproduce

Use Python 3.10 or newer and Pillow 12.3.0 (also supplied by HA 2026.10.2):

```sh
python -m pip install Pillow==12.3.0
python scripts/generate_brand.py
```

The script needs no network access and produces the same PNG bytes on every
run with that Pillow version.

SHA256 (Pillow 12.3.0):

- `icon@2x.png`: `e6f70f13b59b4f21719ad75d4e33112fc0256e63ac7d9cc5f4caf6bfbaca2dc5`
- `icon.png`: `732b606aef92b1f6757fa33937a1233a9bed28eb9779da49f3cff7636f87db23`
- `logo@2x.png`: `7c5883f3c537b131549c5560d29a9068abda52a76fa32f63e4b473db248e9f69`
- `logo.png`: `59dfef1db984d7b8eb423d1682e4942ddb50782fbea1b9aac44218c0458d15bc`

The local `brand/icon.png` is used by the
[HACS brands check](https://hacs.xyz/docs/publish/include/#check-brands).
These files do not imply inclusion in the HACS default list or HA brands
repository. README pages use `custom_components/kibble/brand/logo.png`.
