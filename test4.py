# 引入 glob
import glob

# 讀取目錄下的所有檔案
read_files = glob.glob('**/*.txt',recursive=True)

# 合併檔案
with open("result.txt", "wb") as outfile:
    for f in read_files:
        with open(f, "rb") as infile:
            outfile.write(infile.read())
