from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options = options)

driver.get("https://music.youtube.com/playlist?list=PLHFKipM1WqI_XG4Ctf3JQDm3lRuMbSiEX&si=6O26KHBsAkqaQcNd")


button = driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/form[1]/div/div')
button.click()

try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="contents"]/ytmusic-responsive-list-item-renderer[1]/div[2]/div[1]/yt-formatted-string/a'))
    )
except:
    pass

content = driver.page_source
soup = BeautifulSoup(content, "html.parser")

listof = soup.select_one('#contents.style-scope ytmusic-playlist-shelf-renderer')

titles_work = listof.select('.title-column.style-scope.ytmusic-responsive-list-item-renderer')
titles = [title.get_text(strip=True) for title in titles_work]

second_list = listof.select(".flex-columns.style-scope.ytmusic-responsive-list-item-renderer")

artists = []

for song in second_list:
    finding = song.select_one(".flex-column.style-scope.ytmusic-responsive-list-item-renderer.complex-string")
    artists.append(finding)
    
