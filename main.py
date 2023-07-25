import os
from random import choice, randint, random
from PIL import Image, ImageDraw

images_count = 10
bas_folder = "./head"
yuz_folder = "./hand"
karakter_folder = "./char"
output_folder = "./images"

# Load karakter_folder images once at the beginning
karakter_images = [Image.open(os.path.join(karakter_folder, f)).convert("RGBA") for f in os.listdir(karakter_folder) if f.endswith(".png")]

def get_random_image_from_folder(folder, used_files):
    image_files = [f for f in os.listdir(folder) if f.endswith(".png") and os.path.join(folder, f) not in used_files]
    return choice(image_files) if image_files else None

def create_random_gradient_image(size):
    gradient_image = Image.new("RGBA", size)
    draw = ImageDraw.Draw(gradient_image)

    color1 = (randint(0, 255), randint(0, 255), randint(0, 255))
    color2 = (randint(0, 255), randint(0, 255), randint(0, 255))

    draw.rectangle([(0, 0), size], fill=color1, outline=None)
    for y in range(size[1]):
        r, g, b = (
            color1[j] + (color2[j] - color1[j]) * y // size[1] for j in range(3)
        )
        draw.line([(0, y), (size[0], y)], fill=(int(r), int(g), int(b)))

    return gradient_image

def create_character_image():
    used_files = set()

    # Randomly choose whether to include karakter folder or not
    include_karakter = randint(0, 1)

    # Include karakter folder and choose an image from it
    if include_karakter:
        karakter_image_path = os.path.join(karakter_folder, get_random_image_from_folder(karakter_folder, used_files))
        karakter_image = Image.open(karakter_image_path).convert("RGBA")
    else:
        karakter_image = choice(karakter_images)

    # Calculate the probability for other folders
    other_folder_prob = 2  # You can adjust this probability as desired

    # Randomly choose whether to include bas_folder images or not
    include_bas = random() < other_folder_prob
    if include_bas:
        bas_image_path = os.path.join(bas_folder, get_random_image_from_folder(bas_folder, used_files))
        bas_image = Image.open(bas_image_path).convert("RGBA")
    else:
        bas_image = None

    # Randomly choose whether to include yuz_folder images or not
    include_yuz = random() < other_folder_prob
    if include_yuz:
        yuz_image_path = os.path.join(yuz_folder, get_random_image_from_folder(yuz_folder, used_files))
        yuz_image = Image.open(yuz_image_path).convert("RGBA")
    else:
        yuz_image = None

    # Create a random gradient background
    image_size = (karakter_image.width, karakter_image.height)
    gradient_image = create_random_gradient_image(image_size)

    # Composite the images
    combined_image = Image.alpha_composite(gradient_image, karakter_image)

    if include_yuz and yuz_image:
        combined_image = Image.alpha_composite(combined_image, yuz_image)

    # Move the bas_image (head) to the top layer of the character
    if include_bas and bas_image:
        combined_image = Image.alpha_composite(combined_image, bas_image)

    return combined_image

for i in range(images_count):
    try:
        character_image = create_character_image()
    except ValueError as e:
        print(e)
        continue

    file_name = f"character_{i}.png"
    character_image.save(os.path.join(output_folder, file_name))
