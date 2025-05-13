from PIL import Image, ImageEnhance

def run():
    # 打开并转为灰度
    img = Image.open("RGBoutput.jpg").convert("L")

    # ✴️ 加深图像（调整对比度 > 1.0 会让图像对比度更高）
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.5)  # 1.2 = 对比度提高

    # 创建 16 灰阶调色板
    palette = []
    step = 255 // 15
    for i in range(16):
        val = i * step
        palette.extend([val] * 3)
    palette.extend([0] * (768 - len(palette)))

    # 建立调色板图像
    pal_img = Image.new("P", (1, 1))
    pal_img.putpalette(palette)

    # 应用抖动 + 限制为 16 灰阶
    dithered = img.convert("RGB").quantize(palette=pal_img, dither=Image.FLOYDSTEINBERG)

    # 转回 RGB 并旋转
    rotated = dithered.convert("L").rotate(-90, expand=True)

    # 保存
    rotated.save("Grayoutput.jpg", "JPEG")
