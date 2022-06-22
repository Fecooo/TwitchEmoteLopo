from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import urllib.request
from time import sleep
from colorama import Fore
from colored import fg
zold=fg('green')

options = Options()
options.add_argument('--log-level=3')
options.add_argument("--disable-notifications")

PATH = "C:\Program Files (x86)\chromedriver.exe"


# indítás
print(Fore.WHITE + " --> " + Fore.GREEN + "A program segítségével adott Twitch csatornáról tudod megszerezni az emoteokat fájlként!")
print(Fore.WHITE + " --> " + Fore.GREEN + "Az összes csatornán szereplő emote-ot megszerezheted, kivéve a bit-tel feloldhatóakat.")

csatorna = input(Fore.WHITE + " --> " + Fore.GREEN + "Add meg a Twitch csatorna nevét: " + Fore.LIGHTBLUE_EX + "")
hely = input(Fore.WHITE + " --> " + Fore.GREEN + "Add meg a mentési mappa helyének elérési címét: " + Fore.LIGHTBLUE_EX + "")

driver = webdriver.Chrome(options=options, executable_path=PATH)
driver.maximize_window()
driver.get(f"https://www.twitch.tv/{csatorna}")
sleep(2)
html_source = driver.page_source

cookie = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div/div/div[3]/button')
cookie.click()
sleep(3)

chathez = driver.find_elements(By.TAG_NAME, 'a')
chatl = []
for i in chathez:
    if i.get_attribute("class") == "ScInteractive-sc-18v7095-0 kMHbQR InjectLayout-sc-588ddc-0 ctvvYR":
        chatl.append(i)

for i in range(1):
    if f"/{csatorna}/about" in html_source:
        chatl[3].click()
    else:
        break
sleep(4)

emote = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div[1]/div[2]/div/div[1]/div/div/div/div/div/section/div/div[5]/div[2]/div[1]/div[2]/div/div/div[3]/div/div/div/button")
emote.click()
sleep(2)
# indítás vége


# név kiszedő
buttons = driver.find_elements(By.TAG_NAME, 'button')
classok = []
for i in buttons:
    if i.get_attribute("class") == "InjectLayout-sc-588ddc-0 ecWTap emote-button__link":
        classok.append(i)

emote_nevek = []
for i in classok:
    emote_nevek.append(i.get_attribute("aria-label"))
# név kiszedő vége


# kép kiszedő
kepek = []
osszemote = []
images = driver.find_elements(By.TAG_NAME, 'img')
for image in images:
    kepek.append(image.get_attribute('srcset'))

for i in kepek:
    if i.startswith('https://static-cdn.jtvnw.net/emoticons/'):
        osszemote.append(i)

osszemotesplit = [i.split(",")[2] for i in osszemote]

szuro = []

for i in osszemotesplit:
    if i.endswith("3.0x"):
        szuro.append(i.replace("3.0x", ""))
# kép kiszedő vége


# mentés
for i in range(0, len(szuro)):
    if "https://static-cdn.jtvnw.net/emoticons/v2/emotesv2_" in szuro[i]:
        urllib.request.urlretrieve(szuro[i], f"{hely}\{emote_nevek[i]}.gif")
    else:
        urllib.request.urlretrieve(szuro[i], f"{hely}\{emote_nevek[i]}.png")
input("")
driver.close()
# mentés vége