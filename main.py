from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import urllib.request
from colorama import Fore
from colored import fg
zold=fg('green')

options = Options()
options.add_argument('--log-level=3')
options.add_argument("--disable-notifications")

PATH = "C:\Program Files (x86)\chromedriver.exe"

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
sleep(2)

for i in range(1):
    if f"/{csatorna}/about" in html_source:
        chat = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/main/div[2]/div[3]/div/div/div[1]/div[1]/div[2]/div/div[2]/div[2]/div/div/ul/li[5]/a')
        chat.click()
    else:
        break
sleep(7)

html_source = driver.page_source

"""styles = driver.find_elements(By.TAG_NAME, 'div')
for id in styles:
    if id.get_attribute('style') == "width: fit-content;":
        csati = id.get_attribute("id")
print(csati)

eleres = f'//*[@id="{csati}"]/div/div[1]/div/div/div/div/div/section/div/div[5]/div[2]/div[1]/div[3]/div/div/div[3]/div/div/div/button'"""

emote = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div[1]/div[2]/div/div[1]/div/div/div/div/div/section/div/div[5]/div[2]/div[1]/div[2]/div/div/div[3]/div/div/div/button")
emote.click()
sleep(2)

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

szamlalo = 1
for i in szuro:
    if "https://static-cdn.jtvnw.net/emoticons/v2/emotesv2_" in i:
        urllib.request.urlretrieve(i, f"{hely}\{szamlalo}.gif")
    else:
        urllib.request.urlretrieve(i, f"{hely}\{szamlalo}.png")
    szamlalo += 1
input("")
driver.close()