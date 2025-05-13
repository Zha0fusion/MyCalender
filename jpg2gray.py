from PIL import Image

# 使用 Pillow 转为灰阶
def run():
    img = Image.open("RGBoutput.jpg").convert("L")  # "L" 表示灰度模式
    img.save("Grayoutput.jpg", "JPEG")