from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import bs4 as bs
import time

linkNum = int(input('Please place the flashcard set number here: '))
link = 'https://quizlet.com/' + str(linkNum) + '/'
tileValues = []
matches = []
wordsDefs = {}
index = 0

EMAIL = ''          # enter email
PASSWORD = ''       # enter password

# Using the latest driver for Chrome
driver = webdriver.Chrome()

#Establishes wait time
wait = WebDriverWait(driver, 30)

class tilesClass():
    def __init__(self, value, position):
        global tileValues
        global matches
        # The value on the tile (either a word or definition)
        self.text = value.replace('\n', '')
        # The position of the tile in the HTML source
        self.position = position
        # Places the tile's value in a list so that we can find the match's position
        # easier (see line 38)
        tileValues.append(self.text)

    def findMatch(self):
        # If the tile was already matched, don't match it again
        if self.position in matches:
            return
        # Checks to see if the tile's match is a VALUE in the dictionary
        match = wordsDefs.get(self.text)
        # Checks to see if the tile's match is a KEY in the dictionary
        if match == None:
            match = list(wordsDefs.keys())[list(wordsDefs.values()).index(self.text)]
        # Places both the tile and it's match's positions in a list so that the program
        # knows which order to click each tile in
        matches.append(self.position)
        matches.append(tileValues.index(match) + 1)   

def waitThenFind(by, identifier):
    wait.until(EC.visibility_of_element_located((by, identifier)))
    element = driver.find_element(by, identifier)
    return element


driver.get(link)
    
driver.implicitly_wait(2)

driver.maximize_window()

# Finds and clicks the "Login" button
waitThenFind(By.XPATH, '//*[@id="TopNavigationReactTarget"]/header/div/div[2]/div[3]/button').click()

# Finds and clicks the "Sign in with Google" button
waitThenFind(By.XPATH, '//div[text()="Log in with Google"]//parent::span//parent::a').click()

# Finds and types inside the email text box 
waitThenFind(By.CSS_SELECTOR, 'input.whsOnd').send_keys(EMAIL)

print('done typing')

# Finds and clicks the "next" button to bring the user to the password screen
waitThenFind(By.XPATH, '//*[@id="identifierNext"]/div/button').click()

# Finds and types inside the password text box
waitThenFind(By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input').send_keys(PASSWORD)

# Finds and clicks the last "next" button, which finally brings us back to the screen with
# the flashcards and all of the options to click on
waitThenFind(By.ID, 'passwordNext').click()

wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@aria-label="Close modal"]')))
    
# Resetting the index variable, words and definitions dictionary, and words list
index = 0
wordsDefs = {}
words = []
    
# Formatting all of the HTML so that BeautifulSoup4 can use it
soup = bs.BeautifulSoup(driver.page_source, 'html.parser')

# Putting all of the terms in a list
for word in soup.find_all('a', class_='SetPageTerm-wordText'):
    print(word.contents[0])
    words.append(word.contents[0].text.replace('\n', ''))

print('words:', words)

# Adding the terms and each matching definition to a key pair dictionary
for definition in soup.find_all('a', class_='SetPageTerm-definitionText'):
    print(definition.contents[0].text.replace('\n', ''))
    wordsDefs[words[index]] = definition.contents[0].text.replace('\n', '')
    index += 1

print('wordsDefs:', wordsDefs)

# Resets three lists
tileClasses = []
tileValues = []
matches = []
    
driver.get(link + 'micromatch')
waitThenFind(By.XPATH, '/html/body/div[5]/div/div/div/div[2]/button').click()

wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.MatchModeQuestionGridTile-content')))

# Formats the HTML so that BeautifulSoup4 can handle it
soup = bs.BeautifulSoup(driver.page_source, 'html.parser')

# Finds all the tiles that are present on the screen
index = 0
for div in soup.find_all('div', class_='MatchModeQuestionGridTile-content'):
    # Index variable is added to itself so that the positions line up
    index += 1
    # Each tile becomes an instance of the class above and is inserted into a list called
    # "tileClasses"
    print('tile: ', div.contents[0]['aria-label'])
    tileClasses.append(tilesClass(div.contents[0]['aria-label'], index))

print('TILEVALUES:', tileValues)

# Loops through each tile and makes it go through the "findMatch" procedure inside the
# "tilesClass" class above
for tile in tileClasses:
    tile.findMatch()

print(matches)

# Loops the same amount of times that there are tiles on the screen (usually 12)
for x in range(0, len(matches)):
# Finds the tile that is specified in the "matches" list to click on. The tiles were
# put into a list in a certain order (seen above) so that they could be clicked in order
    tileToClick = driver.find_element_by_xpath(f'//div[@class="MatchModeQuestionGridBoard-tile"][{matches[x]}]')
    tileToClick.click()
    print('Click!')

print('Finished in ' + waitThenFind(By.TAG_NAME, 'strong').text + '!')