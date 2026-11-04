"""Draw the document counter icon for both the desktop window and EXE."""

from __future__ import annotations

from PIL import Image, ImageDraw, ImageFont


def render_icon(size: int = 256) -> Image.Image:
    image = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((6, 6, 250, 250), radius=51, fill="#143664")
    draw.rounded_rectangle((15, 15, 241, 241), radius=42, fill="#21568c")

    # Overlapping sheets and a folded corner are legible at taskbar sizes.
    draw.rounded_rectangle((73, 45, 198, 203), radius=11, fill="#85add1")
    draw.rounded_rectangle((50, 30, 183, 196), radius=12, fill="#f8fcff")
    draw.polygon([(142, 31), (183, 72), (142, 72)], fill="#bbdff0")
    draw.line([(142, 31), (142, 72), (183, 72)], fill="#90bed8", width=3)
    for y, width in ((91, 79), (113, 88), (135, 68)):
        draw.rounded_rectangle((70, y, 70 + width, y + 8), radius=4, fill="#9cbad0")

    draw.ellipse((136, 147, 229, 240), fill="#0a2b48")
    draw.ellipse((131, 141, 226, 236), fill="#00a9b4")
    try:
        font = ImageFont.truetype("arialbd.ttf", 57)
    except OSError:
        font = ImageFont.load_default(size=57)
    draw.text((179, 186), "12", font=font, fill="white", anchor="mm")
    if size != 256:
        image = image.resize((size, size), Image.Resampling.LANCZOS)
    return image