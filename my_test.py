import os
import zipfile
from PIL import Image
from io import BytesIO

path = '陈佳露的简历(20260729).pdf'

with zipfile.ZipFile(path, 'r') as z:
    for name in z.namelist():
        # docx中的图片统一存放在 word/media/ 目录下
        if name.startswith('word/media/'):
            print(f"=== 找到图片: {name} ===")

            # 以二进制方式读取图片数据
            image_data = z.read(name)
            print(f"  大小: {len(image_data)} bytes")

            # 使用PIL打开并展示图片
            try:
                img = Image.open(BytesIO(image_data))
                print(f"  格式: {img.format}, 尺寸: {img.size}, 模式: {img.mode}")
                # ✅ 直接保存到docx同级目录，保留原始文件名
                filename = os.path.basename(name)
                save_path = os.path.join('./', filename)
                img.save(save_path)
                print(f"  💾 已保存至: {save_path}")
            except Exception as e:
                print(f"  ⚠️ 无法作为图片打开: {e}")
