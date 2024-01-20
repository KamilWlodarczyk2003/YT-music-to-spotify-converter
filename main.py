from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import spotipy
from spotipy.oauth2 import SpotifyOAuth

options = Options()

SPOTIPY_CLIENT_ID = "XXXXXXXX"
SPOTIPY_CLIENT_SECRET = "XXXXXXXXXXXXXX"
PLAYLIST_LINK = "https://music.youtube.com/playlist?list=PLHFKipM1WqI_XG4Ctf3JQDm3lRuMbSiEX"

#options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options = options)

driver.get(PLAYLIST_LINK)


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

name = soup.select_one("h2.style-scope.ytmusic-detail-header-renderer").get_text(strip=True)

listof = soup.select_one('#contents.style-scope ytmusic-playlist-shelf-renderer')

titles_work = listof.select('.title-column.style-scope.ytmusic-responsive-list-item-renderer')
titles = [title.get_text(strip=True) for title in titles_work]

second_list = listof.select(".flex-columns.style-scope.ytmusic-responsive-list-item-renderer")

artists = []


for song in second_list:
    finding = song.select_one(".flex-column.style-scope.ytmusic-responsive-list-item-renderer.complex-string")
    artists.append(finding.get_text(strip=True))
    
sp = spotipy.Spotify(
    auth_manager= SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt",
        username="XXXX", 
    )
)
user_id = sp.current_user()["id"]

song_uris = []

for x in range(len(titles)):
    result = sp.search(q=f"track:{titles[x]} artist:{artists[x]}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{titles[x]} couldn't find it. Skipped.")
        

playlist = sp.user_playlist_create(user=user_id, name=name, public=False)

if len(titles) > 99:
    n = 0
    while n < len(titles):
        sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris[n])
        n+=1
else:
    sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
    
print(titles)
print(artists)