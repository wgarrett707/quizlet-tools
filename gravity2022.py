from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import bs4 as bs
import time

link = input('Please place the link to the flashcard screen here: ')

tileClasses = []
tileValues = []
words = []
matches = []
wordsDefs = {}
index = 0

EMAIL = ''          # enter email
PASSWORD = ''       # enter password

def findMatch(text):
    # Checks to see if the tile's match is a VALUE in the dictionary
    match = wordsDefs.get(text)
    # Checks to see if the tile's match is a KEY in the dictionary
    if match == None:
        match = list(wordsDefs.keys())[list(wordsDefs.values()).index(text)]
    return match

def waitThenFind(by, identifier):
    wait.until(EC.visibility_of_element_located((by, identifier)))
    element = driver.find_element(by, identifier)
    return element

# Using Chrome to access web
driver = webdriver.Chrome()

#Establishes wait time
wait = WebDriverWait(driver, 30)

# Open the website
driver.get(link)

driver.maximize_window()

# Formatting all of the HTML so that BeautifulSoup4 can use it
soup = bs.BeautifulSoup(driver.page_source, 'html.parser')

# Putting all of the terms in a list
for word in soup.find_all('a', class_='SetPageTerm-wordText'):
    words.append(word.contents[0].text.replace('\n', ''))

# Adding the terms and each matching definition to a key pair dictionary
for definition in soup.find_all('a', class_='SetPageTerm-definitionText'):
    wordsDefs[words[index]] = definition.contents[0].text.replace('\n', '')
    index += 1

print(wordsDefs)

# Resetting the index variable to use it again later
index = 0

# Finds and clicks the "Login" button
waitThenFind(By.XPATH, '//*[@id="TopNavigationReactTarget"]/header/div/div[2]/div[3]/button').click()

# Finds and clicks the "Sign in with Google" button
waitThenFind(By.XPATH, '//div[text()="Log in with Google"]//parent::span//parent::a').click()

# Finds and types inside the email text box 
waitThenFind(By.CSS_SELECTOR, 'input.whsOnd').send_keys(EMAIL)

# Finds and clicks the "next" button to bring the user to the password screen
waitThenFind(By.XPATH, '//*[@id="identifierNext"]/div/button').click()

# Sleeps for 2 seconds because it tries to look for the password box before the page loads

# Finds and types inside the password text box
waitThenFind(By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input').send_keys(PASSWORD)

# Finds and clicks the last "next" button, which finally brings us back to the screen with
# the flashcards and all of the options to click on
waitThenFind(By.ID, 'passwordNext').click()

waitThenFind(By.CSS_SELECTOR, 'div.c13e2cpr > svg').click()

# Selects the "gravity" button
waitThenFind(By.XPATH, '//*[@id="setPageSetIntroWrapper"]/div/div/div[2]/nav/div/div[2]/span[2]/a').click()

# Finds and clicks the "Start Game" button for the gravity game
GetStarted = driver.find_element_by_css_selector('button.UIButton--hero')

GetStarted.click()

HardButton = driver.find_element_by_xpath('//input[@aria-label="EXPERT"]')

HardButton.click()

LetsGoButton = driver.find_element_by_css_selector('div.GravityOptionsView-nextButtonWrapper')

LetsGoButton.click()

StartGame = driver.find_element_by_css_selector('button.UIButton.UIButton--hero')

StartGame.click()

InputBox = driver.find_element_by_tag_name('textarea')

while True:
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.GravityTerm-text')))
    start = time.time()
    #soup = bs.BeautifulSoup(driver.page_source, 'html.parser')
    #AsteroidText = soup.find('span', class_='TermText')
    #InputBox.send_keys(findMatch(AsteroidText.text))
    termSpan = driver.find_element(By.CSS_SELECTOR, 'span.TermText')
    InputBox.send_keys(findMatch(termSpan.text))
    InputBox.send_keys(Keys.ENTER)
    end = time.time()
    print('Time taken:', end - start)