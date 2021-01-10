from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import os

print("""
    _______        ____     |    __  __                _                   _                   
   / _____ \      /___ \    |   |  \/  | ___  ___ __ _| |_ _ __ ___  _ __ (_) __ _ _   _  ___  
  / /     \ \         \ \   |   | |\/| |/ _ \/ __/ _` | __| '__/ _ \| '_ \| |/ _` | | | |/ _ \  
 / /       \ \         \ \  |   | |  | |  __/ (_| (_| | |_| | | (_) | | | | | (_| | |_| |  __/ 
 | |        \ \        | |  |   |_|  |_|\___|\___\__,_|\__|_|  \___/|_| |_|_|\__, |\__,_|\___| 
 \ \         \ \       / /  |                                                   |_|            
  \ \____     \ \_____/ /   |  
   \____/      \_______/    |             Mechatronics CLUB <<ENSET MOHAMMEDIA>>
   

    thia script was made by KOUSTA KHALID for the Python Training
    Gmail : kousta90@gmail.com
    date : 08/01/2021

""")

time.sleep(2)

website = 'https://e-bourse-maroc.onousc.ma/'
cne = "put your cne here"


browser = webdriver.Chrome()
browser.get(website)
time.sleep(2)

browser.maximize_window() # maximise the size of the window
time.sleep(1)

body = browser.find_element_by_css_selector('body')
body.send_keys(Keys.PAGE_DOWN)
time.sleep(1)

cycle_etude = browser.find_element_by_name('type')
cycle_etude.click()
time.sleep(1)

cycle_etude = browser.find_element_by_xpath("//*[@id='one']/div/form/center/div/table/tbody/tr[2]/td[2]/select/option[2]")
cycle_etude.click()
time.sleep(1)

Annee_bac = browser.find_element_by_name('abac')
Annee_bac.click()
time.sleep(1)

cycle_etude = browser.find_element_by_xpath("//*[@id='one']/div/form/center/div/table/tbody/tr[3]/td[2]/select/option[17]")
cycle_etude.click()
time.sleep(1)

CNE = browser.find_element_by_name('cne')
CNE.send_keys(cne + Keys.RETURN)
time.sleep(1)

body = browser.find_element_by_css_selector('body')
body.send_keys(Keys.PAGE_DOWN)
time.sleep(1)

browser.get_screenshot_as_file("bourse.png")

time.sleep(2)
browser.quit()
