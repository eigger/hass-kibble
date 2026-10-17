# Kibble brand assets

`icon@2x.png` is an unmodified copy of the 512 × 512 PNG app icon from
[eigger/kibble](https://github.com/eigger/kibble/blob/882038604dbd4272c02d6330230df36d824129ba/apps/web/public/icons/icon-512.png).
`icon.png` is its 256 × 256 RGBA derivative using Pillow's LANCZOS resize.
These sizes follow the [HA brand image guidelines](https://contributors.home-assistant.io/core/integrations/brands/).

Source revision: `882038604dbd4272c02d6330230df36d824129ba`.
Copyright (c) 2026 eigger. MIT licensed; the matching copyright and license
notice is retained in this repository's [LICENSE](../../../LICENSE).

Reproduce using the pinned current test environment (Pillow 12.3.0, supplied
by HA 2026.10.2), from the repository root:

```sh
.venv/bin/python scripts/generate_brand.py
```

SHA256:

- `icon@2x.png`: `f3dde0298478cf30ee07a93b905c2debf796c430eb0cbd29f7c8e38983d329ba`
- `icon.png`: `a2cf1524b626ff284de868c0f25dc9c99cf94447e1b7bf363f9b251c298efd59`

The local `brand/icon.png` is used by the
[HACS brands check](https://hacs.xyz/docs/publish/include/#check-brands).
It does not imply inclusion in the HACS default list or HA brands repository.
