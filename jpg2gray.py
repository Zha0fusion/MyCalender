from PIL import Image

# 使用 Pillow 转为灰阶 + 旋转
def run():
    # 打开并转换为灰度图像
    img = Image.open("RGBoutput.jpg").convert("L")  # "L" = 灰阶

    # 顺时针旋转 90 度（rotate 默认是逆时针，所以用 -90）
    rotated = img.rotate(-90, expand=True)

    # 保存输出
    rotated.save("Grayoutput.jpg", "JPEG")