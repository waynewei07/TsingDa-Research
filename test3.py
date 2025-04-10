# 引用 BeautifulSoup
import os
from bs4 import BeautifulSoup

# 本地資料夾
your_dir = "/home/wayne/desktop/課程逐字搞"
your_dir2 = "/home/wayne/desktop/課程逐字搞txt"

for folder in os.listdir(your_dir):
    for file in os.listdir(os.path.join(your_dir, folder)):

        # 掃描所有 html 檔案
        if file.endswith((".htm", ".html")):

            # 使用 BeautifulSoup 更改檔案屬性
            with open(os.path.join(your_dir, folder, file), encoding='utf-8',errors='ignore') as markup:
                soup = BeautifulSoup(markup.read(),features="html.parser")
            with open(os.path.join(your_dir2, folder, file.split(".")[0]+".txt"), "w", encoding='utf-8',errors='ignore') as f:
                f.write(soup.get_text())
