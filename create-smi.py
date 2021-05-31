from PIL import Image
import os

video_name = "butter"
fps = 23.980618307905036
file_format = "jpg"


class termcolor:
    OKGREEN = "\033[92m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"


class braille_config:
    # 2 * 3 braille
    base = 0x2800
    width = 2
    height = 3


class video_config:
    width = 56
    height = 24
    frame_jump = 3  # reduces framerate by 3


def resize(image: Image.Image, width: int, height: int) -> Image.Image:
    if height == 0:
        height = int(im.height / im.width * width)
    if height % braille_config.height != 0:
        height = int(braille_config.height * (height // braille_config.height))
    if width % braille_config.width != 0:
        width = int(braille_config.width * (width // braille_config.width))
    return image.resize((width, height))


def grayscale(red: int, green: int, blue: int) -> int:
    return int(0.2126 * red + 0.7152 * green + 0.0722 * blue)


def convert_timedelta_to_srt_format(delta_in_ms: float, framecount: int):
    time = delta_in_ms * framecount
    return int(time)


hex_threshold = 128
frames_folder = sorted(os.listdir(os.getcwd() + "/frames/" + video_name))
one_frame_in_ms = 1000.0 / fps
terminal_columns, terminal_rows = os.get_terminal_size(0)

smi_string = """
<SAMI>
<HEAD>
P {font-family: sans-serif; color:white;}
.KOKRCC {Name: 'Korean Captions'; lang: ko-KR; SAMIType: CC;}
</HEAD>
<BODY>
"""
with open(f"{video_name}.smi", "a", encoding="UTF-8") as file:
    file.write(smi_string + "\n")

for idx in range(0, len(frames_folder), video_config.frame_jump):
    normalized_path = os.path.abspath(
        f"{os.getcwd()}/frames/{video_name}/f{idx}.{file_format}"
    )
    im = Image.open(normalized_path)

    # (image, weight, height). 0 as height means auto
    resized_image = resize(im, video_config.width, video_config.height)

    px = resized_image.load()
    terminal_string = f"{idx + 1}\n"
    terminal_string += f"{convert_timedelta_to_srt_format(one_frame_in_ms, idx)} --> {convert_timedelta_to_srt_format(one_frame_in_ms, idx + 1)}\n"

    smi_string = f"<SYNC Start={convert_timedelta_to_srt_format(one_frame_in_ms, idx)}><P Class=KOKRCC>"

    color_stack_color = ""
    color_stack_value = ""

    for h in range(0, resized_image.height, braille_config.height):
        for w in range(0, resized_image.width, braille_config.width):
            braille = [False] * braille_config.width * braille_config.height
            braille_r = 0
            braille_g = 0
            braille_b = 0
            for local_w in range(braille_config.width):
                for local_h in range(braille_config.height):
                    r, g, b, *rest = px[w + local_w, h + local_h]  # ignore alpha
                    braille_r += r
                    braille_g += g
                    braille_b += b
                    if grayscale(r, g, b) > hex_threshold:
                        braille[local_w * braille_config.height + local_h] = True
            output = braille_config.base
            for b_idx, val in enumerate(braille):
                if val:
                    output += 2 ** b_idx
            braille_r //= braille_config.width * braille_config.height
            braille_g //= braille_config.width * braille_config.height
            braille_b //= braille_config.width * braille_config.height
            terminal_string += "\033[38;2;{};{};{}m{}\033[38;2;255;255;255m".format(
                braille_r, braille_g, braille_b, chr(output)
            )
            hex_color = "#%02X%02X%02X" % (braille_r, braille_g, braille_b)
            if color_stack_color == hex_color:
                color_stack_value += chr(output)
            else:
                if color_stack_value != "":
                    smi_string += (
                        f'<FONT color="{color_stack_color}">'
                        + color_stack_value
                        + "</FONT>"
                    )
                color_stack_color = hex_color
                color_stack_value = chr(output)
        smi_string += (
            f'<FONT color="{color_stack_color}">' + color_stack_value + "</FONT>"
        )
        color_stack_color = ""
        color_stack_value = ""
        terminal_string += "\n"
        smi_string += "<BR>"
    smi_string += "</SYNC>"
    with open(f"{video_name}.smi", "a", encoding="UTF-8") as file:
        file.write(smi_string + "\n")
    print(terminal_string)
with open(f"{video_name}.smi", "a", encoding="UTF-8") as file:
    file.write("</BODY>")
    file.write("</SAMI>")
