import uuid
from PIL import Image, ImageDraw, ImageFont


def get_wrapped_text(text: str, line_length: int, font: ImageFont):

    lines = [""]

    for word in text.split(" "):

        line = f"{lines[-1]} {word}".strip()

        if font.getlength(line) <= line_length:
            lines[-1] = line
        else:
            lines.append(word)

    return lines


def make_no_yes_meme(user_texts: list, font_size: int, template_name: str, pos1: tuple, pos2: tuple,
                     max_line_length: int):

    with Image.open(f"templates/{template_name}") as img:

        draw = ImageDraw.Draw(img)
        first_text_box = user_texts[0]
        second_text_box = user_texts[1]
        font = ImageFont.truetype("arial.ttf", font_size)

        first_text_lines = get_wrapped_text(text=first_text_box, line_length=max_line_length, font=font)
        second_text_lines = get_wrapped_text(text=second_text_box, line_length=max_line_length, font=font)

        if len(first_text_lines) > 10 or len(second_text_lines) > 10:
            print("Слишком длинный текст")
            return "Текст слишком длиный для этого шаблона..."

        y = pos1[1]

        for line in first_text_lines:
            draw.text(xy=(pos1[0], y), text=line, font=font, fill="black")
            y += font.size

        y = pos2[1]
        for line in second_text_lines:
            draw.text(xy=(pos2[0], y), text=line, font=font, fill="black")
            y += font.size

        random_name = f"{uuid.uuid4().hex}.png"
        img.save(f"user_memes/{random_name}")

        return random_name

