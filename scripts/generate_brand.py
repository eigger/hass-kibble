"""Generate Home Assistant brand images for Kibble.

The artwork preserves the original Kibble warm amber rounded-square palette and
white paw mark, refined with sculpted angled toe pads and a contoured main pad
at 4x scale, paired with a matching amber Kibble wordmark for the landscape
logo. No source image, external font file, or network access is needed. Run with
Pillow 12.3.0 for reproducible PNGs.
"""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

BRAND = Path(__file__).resolve().parents[1] / "custom_components/kibble/brand"
SIZE = 512
SCALE = 4
AMBER = "#c47a2c"
WHITE = "#ffffff"
WORDMARK = "#c47a2c"


def _draw_rotated_oval(
    d: ImageDraw.ImageDraw,
    cx: float,
    cy: float,
    rx: float,
    ry: float,
    angle_deg: float,
    fill: str,
) -> None:
    """Draw a smooth rotated ellipse as a high-density polygon."""
    steps = 64
    rad = math.radians(angle_deg)
    ca, sa = math.cos(rad), math.sin(rad)
    pts = []
    for i in range(steps):
        t = 2.0 * math.pi * i / steps
        x = rx * math.cos(t)
        y = ry * math.sin(t)
        pts.append((cx + x * ca - y * sa, cy + x * sa + y * ca))
    d.polygon(pts, fill=fill)


def draw_icon() -> Image.Image:
    """Draw the 512px RGBA app icon."""
    s = SCALE
    image = Image.new("RGBA", (SIZE * s, SIZE * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(image)

    def box(x0: float, y0: float, x1: float, y1: float) -> list[float]:
        return [x0 * s, y0 * s, x1 * s, y1 * s]

    # 1. Warm amber rounded square background (matching upstream Kibble palette).
    d.rounded_rectangle(box(0, 0, SIZE - 1, SIZE - 1), radius=104 * s, fill=AMBER)

    # 2. Centered white paw print with well-separated angled toe pads and contoured main pad.
    _draw_rotated_oval(d, 134 * s, 214 * s, 32 * s, 44 * s, -24, WHITE)
    _draw_rotated_oval(d, 212 * s, 152 * s, 33 * s, 46 * s, -8, WHITE)
    _draw_rotated_oval(d, 300 * s, 152 * s, 33 * s, 46 * s, 8, WHITE)
    _draw_rotated_oval(d, 378 * s, 214 * s, 32 * s, 44 * s, 24, WHITE)

    # Contoured three-lobed main pad centered below the toes.
    d.ellipse(box(194, 228, 318, 344), fill=WHITE)
    d.ellipse(box(148, 268, 262, 372), fill=WHITE)
    d.ellipse(box(250, 268, 364, 372), fill=WHITE)
    d.rounded_rectangle(box(180, 296, 332, 372), radius=28 * s, fill=WHITE)

    return image.resize((SIZE, SIZE), Image.Resampling.LANCZOS)


def main() -> None:
    """Write icon.png, icon@2x.png, logo.png and logo@2x.png."""
    BRAND.mkdir(parents=True, exist_ok=True)
    icon = draw_icon()
    icon.save(BRAND / "icon@2x.png", optimize=True)
    icon.resize((256, 256), Image.Resampling.LANCZOS).save(
        BRAND / "icon.png", optimize=True
    )

    # Pillow bundles Aileron Regular, so regeneration needs no system fonts.
    font = ImageFont.load_default(size=432)
    bounds = font.getbbox("Kibble")
    wordmark = Image.new("RGBA", (bounds[2] - bounds[0], bounds[3] - bounds[1]))
    ImageDraw.Draw(wordmark).text(
        (-bounds[0], -bounds[1]), "Kibble", font=font, fill=WORDMARK
    )
    wordmark = wordmark.crop(wordmark.getbbox())
    gap = 96 + ((SIZE + 96 + wordmark.width) % 2)
    logo = Image.new("RGBA", (SIZE + gap + wordmark.width, SIZE))
    logo.alpha_composite(icon, (0, 0))
    logo.alpha_composite(wordmark, (SIZE + gap, (SIZE - wordmark.height) // 2))
    logo = logo.crop(logo.getbbox())
    logo.save(BRAND / "logo@2x.png", optimize=True)
    logo.resize((logo.width // 2, logo.height // 2), Image.Resampling.LANCZOS).save(
        BRAND / "logo.png", optimize=True
    )


if __name__ == "__main__":
    main()
