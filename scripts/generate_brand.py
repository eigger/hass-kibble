"""Generate the 256px HA icon from Kibble's preserved 512px source asset."""

from pathlib import Path

from PIL import Image

brand = Path(__file__).resolve().parents[1] / "custom_components/kibble/brand"
with Image.open(brand / "icon@2x.png") as source:
    if source.size != (512, 512) or source.mode != "RGBA":
        raise ValueError("Expected the original 512px RGBA Kibble app icon")
    source.resize((256, 256), Image.Resampling.LANCZOS).save(brand / "icon.png")
