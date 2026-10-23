# Kibble brand assets

The original Kibble paw icon and amber color are preserved. The landscape logo
pairs that icon with a matching amber `Kibble` wordmark on a transparent
background. It is a layout derivative for this integration, not an upstream
Kibble wordmark.

| File | Size | Purpose |
| --- | --- | --- |
| `icon.png` | 256 × 256 | Home Assistant and HACS icon |
| `icon@2x.png` | 512 × 512 | Preserved original app icon; high-resolution icon |
| `logo.png` | 938 × 256 | Landscape integration logo; README artwork |
| `logo@2x.png` | 1876 × 512 | High-resolution landscape logo |

All images are RGBA PNGs, with transparent outer corners/backgrounds. These
sizes follow the [HA brand image guidelines](https://contributors.home-assistant.io/core/integrations/brands/).
Home Assistant 2026.3 and later serves these assets from the integration's local
`brand/` directory. The amber wordmark works against light and dark backgrounds,
so separate dark variants are not required.

## Source and permission

`icon@2x.png` is an unmodified copy of the 512 × 512 PNG app icon from
[eigger/kibble](https://github.com/eigger/kibble/blob/882038604dbd4272c02d6330230df36d824129ba/apps/web/public/icons/icon-512.png).
Source revision: `882038604dbd4272c02d6330230df36d824129ba`.
Copyright (c) 2026 eigger. MIT licensed; the matching copyright and license
notice is retained in this repository's [LICENSE](../../../LICENSE).

The wordmark is rendered with Pillow's bundled Aileron Regular via
[`ImageFont.load_default`](https://pillow.readthedocs.io/en/stable/reference/ImageFont.html#PIL.ImageFont.load_default).
[Aileron](https://dotcolon.net/font/aileron/) permits commercial use and is
released with no rights reserved. No font file is redistributed or loaded from the system.
The icon and logo derivation code is covered by this repository's MIT license.

## Reproduce

Use Python 3.10 or newer and Pillow 12.3.0 (also supplied by HA 2026.10.2):

```sh
python -m pip install Pillow==12.3.0
python scripts/generate_brand.py
```

The script verifies the original icon's SHA256 before creating any derivatives.
It needs no network access after Pillow is installed and keeps the original
`icon@2x.png` unchanged. Running it twice produces the same PNG bytes.

SHA256:

- `icon@2x.png`: `f3dde0298478cf30ee07a93b905c2debf796c430eb0cbd29f7c8e38983d329ba`
- `icon.png`: `a2cf1524b626ff284de868c0f25dc9c99cf94447e1b7bf363f9b251c298efd59`
- `logo@2x.png`: `cfafc3cbe57088b983f1ae2b113ca52670b6d410caab88cf7e867e291245fa6d`
- `logo.png`: `a7e842b5cd3ce4f9892475fe47d9124b49c0d67a06e677910e3f4d40e68ff371`

The local `brand/icon.png` is used by the
[HACS brands check](https://hacs.xyz/docs/publish/include/#check-brands).
These files do not imply inclusion in the HACS default list or HA brands
repository. README pages can use `custom_components/kibble/brand/logo.png`.
