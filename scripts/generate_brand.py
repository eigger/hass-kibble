"""Generate Home Assistant brand images from Kibble's preserved app icon.

Run with Pillow 12.3.0 for byte-for-byte reproducible PNGs. No network access,
external font files, or modifications to the 512px source icon are required.
"""

from hashlib import sha256
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

BRAND = Path(__file__).resolve().parents[1] / "custom_components/kibble/brand"
SOURCE_SHA256 = "f3dde0298478cf30ee07a93b905c2debf796c430eb0cbd29f7c8e38983d329ba"


def main() -> None:
    """Preserve the source icon and derive the normal icon and landscape logos."""
    source_path = BRAND / "icon@2x.png"
    if sha256(source_path.read_bytes()).hexdigest() != SOURCE_SHA256:
        raise ValueError("The preserved Kibble source icon has changed")

    with Image.open(source_path) as source:
        if source.size != (512, 512) or source.mode != "RGBA":
            raise ValueError("Expected the original 512px RGBA Kibble app icon")
        source.resize((256, 256), Image.Resampling.LANCZOS).save(BRAND / "icon.png")

        # Pillow bundles Aileron Regular, so regeneration needs no system fonts.
        font = ImageFont.load_default(size=448)
        bounds = font.getbbox("Kibble")
        wordmark = Image.new("RGBA", (bounds[2] - bounds[0], bounds[3] - bounds[1]))
        ImageDraw.Draw(wordmark).text(
            (-bounds[0], -bounds[1]), "Kibble", font=font, fill="#c47a2c"
        )
        gap = 96
        logo = Image.new("RGBA", (512 + gap + wordmark.width, 512))
        logo.alpha_composite(source, (0, 0))
        logo.alpha_composite(wordmark, (512 + gap, (512 - wordmark.height) // 2))
        # Trim the glyph's side bearing, including antialiased edge pixels.
        logo = logo.crop(logo.getbbox())
        logo.save(BRAND / "logo@2x.png", optimize=True)
        logo.resize((logo.width // 2, logo.height // 2), Image.Resampling.LANCZOS).save(
            BRAND / "logo.png", optimize=True
        )


if __name__ == "__main__":
    main()
