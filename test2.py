# 引入 selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


if __name__ == '__main__':

    # 啟用 AdBlocker
    options = Options() 
    options.add_extension('/home/wayne/下載/GIGHMMPIOBKLFEPJOCNAMGKKBIGLIDOM_5_19_0_0.crx')
    driver = webdriver.Chrome(options=options)
    time.sleep(5)

    # 課程的 youtube playlist 網址
    playlist='https://www.youtube.com/playlist?list=PLDA2BC5E785D495AB'
    
    # 第三方網站
    search='https://downsub.com/?url='
    
    wait = WebDriverWait(driver, 5)
    driver.get(playlist)
    len = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="page-manager"]/ytd-browse/ytd-playlist-header-renderer/div/div[2]/div[1]/div/div[1]/div[1]/ytd-playlist-byline-renderer/div/yt-formatted-string[1]/span[1]'))).text
    for i in range(1,int(len)+1):
        driver.get(playlist)

        # 複製影片網址
        a = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="contents"]/ytd-playlist-video-renderer['+str(i)+']')))
        a.click()
        cur = driver.current_url

        # 點擊下載
        driver.get(search+cur)
        b = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="app"]/div/main/div/div[2]/div/div[1]/div[1]/div[2]/div[1]/button[2]')))
        b.click()
        print('Successfully Downloaded '+str(i)+'/'+len+' of Playlist')
