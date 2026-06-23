from PIL import Image, ImageFont, ImageDraw
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_PATH = os.path.join(BASE_DIR, "fonts", "DejaVuSansMono.ttf")
print(FONT_PATH)
print(os.path.exists(FONT_PATH))

ASCII_SETS = {
    "classic": "@%#*+=-:. ",
    "dense": "@$B%8&WM#*oahkbdpqwm",
    "numbers": "9876543210",
    "binary": "01"
}

def image_to_ascii(image_path, width=120, charset="classic"):
    chars = ASCII_SETS.get(charset, ASCII_SETS["classic"])
    img = Image.open(image_path).convert("RGBA")

    aspect_ratio = img.height / img.width
    height = max(1, int(width * aspect_ratio * 0.55))

    # img = img.resize((width, height))
    img = img.resize(
        (width, height),
        Image.Resampling.LANCZOS
    )
    pixels = img.load()

    ascii_art = []

    for y in range(height):
        row = ""
        for x in range(width):
            r, g, b, a = pixels[x, y]

            # Transparent background
            if a < 200:
                row += " "
                continue

            # brightness = int((r + g + b) / 3)
            brightness = int(
                0.299 * r +
                0.587 * g +
                0.114 * b
            )

            brightness = max(
                0,
                min(
                    255,
                    int((brightness - 128) * 1.4 + 128)
                )
            )

            if brightness > 240:
                row += " "
                continue

            idx = brightness * (len(chars) - 1) // 255
            # idx = (255 - brightness) * (len(chars) - 1) // 255
            row += chars[idx]

        ascii_art.append(row)

    return "\n".join(ascii_art)


def ascii_to_image(ascii_art, output_path):

    font_size = 8

    try:
        font = ImageFont.truetype(FONT_PATH, font_size)
    except:
        font = ImageFont.load_default()

    dummy = Image.new("RGBA", (1, 1))
    draw = ImageDraw.Draw(dummy)

    left, top, right, bottom = draw.multiline_textbbox(
        (0, 0),
        ascii_art,
        font=font
    )

    img_width = right - left
    img_height = bottom - top

    image = Image.new("RGBA", (img_width + 10, img_height + 10), (255, 255, 255, 0))

    draw = ImageDraw.Draw(image)

    draw.multiline_text(
        (5, 5),
        ascii_art,
        fill="white",
        font=font
    )

    image.save(output_path)