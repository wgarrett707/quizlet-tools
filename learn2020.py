from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import bs4 as bs
import time

link = input("Please place the link to the flashcard screen here: ")

words = []
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

# Using Chrome to access web
driver = webdriver.Chrome()

driver.implicitly_wait(2)

# Open the website
driver.get(link)

driver.maximize_window()

# Formatting all of the HTML so that BeautifulSoup4 can use it
soup = bs.BeautifulSoup(driver.page_source, 'lxml')

# Putting all of the terms in a list
for word in soup.find_all('a', class_='SetPageTerm-wordText'):
    words.append(word.contents[0].text.replace("\n", ""))

# Adding the terms and each matching definition to a key pair dictionary
for definition in soup.find_all('a', class_='SetPageTerm-definitionText'):
    wordsDefs[words[index]] = definition.contents[0].text.replace("\n", "")
    index += 1

print(wordsDefs)

# Resetting the index variable to use it again later
index = 0

# Finds and clicks the "Login" button
LogIn = driver.find_element_by_xpath("//span[@class='SiteHeader-signInBtn']/parent::*")

LogIn.click()

# Finds and clicks the "Sign in with Google" button
LogInGoogle = driver.find_element_by_css_selector('a.UIButton--social')

LogInGoogle.click()

time.sleep(3)

# Finds and types inside the email text box 
LogInEmailBox = driver.find_element_by_tag_name('input')

LogInEmailBox.send_keys(EMAIL)

# Finds and clicks the "next" button to bring the user to the password screen
LogInNext = driver.find_element_by_xpath("//div[@role='button']")

LogInNext.click()

# Sleeps for 2 seconds because it tries to look for the password box before the page loads
time.sleep(2)

# Finds and types inside the password text box
LogInPassBox = driver.find_element_by_name('password')

LogInPassBox.send_keys(PASSWORD)

# Finds and clicks the last "next" button, which finally brings us back to the screen with
# the flashcards and all of the options to click on
LogInNext2 = driver.find_element_by_id('passwordNext')

LogInNext2.click()

time.sleep(2)

# Selects the "learn" button
LearnButton = driver.find_element_by_xpath("//a[@aria-label='Learn']/child::*")

# Clicks on the "learn" button that was selected earlier
LearnButton.click()

time.sleep(2)

# IF IT TURNS OUT THAT THE "got it" BUTTON DOESN'T APPEAR ALL THE TIME, UNTAG THE CODE BELOW
#soup = bs.BeautifulSoup(driver.page_source, 'lxml')
#GotItButton = soup.find('button', class_='UIButton UIButton--hero')
#print(GotItButton)
#if GotItButton != None:

GotItButton = driver.find_element_by_css_selector("button.UIButton--hero")
GotItButton.click()

# unfinished
restart = True
while restart == True:
    learning = True
    while learning == True:
        time.sleep(1.3)
        soup = bs.BeautifulSoup(driver.page_source, 'lxml')
        HeadingText = soup.find('div', style='display: block;')  
    
        if HeadingText == None:
            print("test")
            ContinueButton = driver.find_element_by_xpath("//div[@class='FixedContinueButton']/child::*")
            ContinueButton.click()
            learning == False

        questionText = HeadingText.text
        InputBox = soup.find('textarea')

        # This is currently broken. It knows which element is right, yet it sometimes
        # clicks a box away from it instead
        if InputBox == None:
            MultipleChoice = soup.find_all('div', class_='MultipleChoiceQuestionPrompt-termOptionInner')
            print(MultipleChoice)
            for option in MultipleChoice:
                index += 1
                optionText = option.contents[0].contents[0].text
                print(optionText)
                if questionText == findMatch(optionText):
                    print("ANSWER ^^^")
                    answerOption = driver.find_element_by_xpath(f"//div[@class='MultipleChoiceQuestionPrompt-termOption'][{index}]")
                    answerOption.click()
                    break
        else:
            InputBox = GotItButton = driver.find_element_by_tag_name("textarea")
            InputBox.send_keys(findMatch(HeadingText.text))
            InputBox.send_keys(Keys.ENTER)    

    
