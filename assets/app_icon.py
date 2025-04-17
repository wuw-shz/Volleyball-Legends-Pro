from PIL import Image, ImageDraw

def create_volleyball_icon():
    img = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    draw.ellipse((20, 20, 236, 236), fill=(255, 255, 255), outline=(0, 0, 0), width=3)
    
    draw.arc((20, 20, 236, 236), start=0, end=360, fill=(50, 50, 50), width=3)
    draw.arc((20, 80, 236, 170), start=0, end=180, fill=(80, 80, 80), width=4)
    draw.arc((20, 80, 236, 170), start=180, end=360, fill=(80, 80, 80), width=4)
    draw.line((20, 128, 236, 128), fill=(80, 80, 80), width=4)
    draw.line((128, 20, 128, 236), fill=(80, 80, 80), width=4)
    
    sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
    
    icon_sizes = []
    for size in sizes:
        resized_img = img.resize(size)
        icon_sizes.append(resized_img)
    
    icon_path = 'assets/app_icon.ico'
    img.save(icon_path, format='ICO', sizes=[(size, size) for size in [16, 32, 48, 64, 128, 256]])
    
    print(f"Icon created successfully: {icon_path}")
    return icon_path

if __name__ == "__main__":
    create_volleyball_icon() 