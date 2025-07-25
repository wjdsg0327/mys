from PIL import Image, ImageDraw

def create_click_circle_image(path="circle.png", size=60):
    img = Image.new("RGBA", (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse((0, 0, size - 1, size - 1), outline=(255, 0, 0, 200), width=4)
    img.save(path)

create_click_circle_image()
