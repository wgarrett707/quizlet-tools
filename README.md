# quizlet-tools

This repository contains automation tools for three of Quizlet's activities. These scripts date back to 2020-2022 and are not currently being supported.

### Stack

This project consists of individual Python scripts. They utilize Selenium for automated web navigation and BeautifulSoup4 for web scraping and parsing. Each of the below scripts logs the user into their Quizlet account, prompts the user for a Quizlet set, and creates a dictionary of matching terms and definitions for the set.

 ### Gravity

 Gravity was a Quizlet game where the user must type in vocabulary words corresponding to definitions contained within asteroids that fall toward the user. The user loses if an asteroid falls out of view of the user's screen before they type in the correct term twice. As levels progress, the asteroids fall faster and faster.

 This game was [retired](https://bfamercury.org/6555/news/quizlets-shift-to-quizlet-plus/#:~:text=%E2%80%9CGravity%2C%E2%80%9D%20however%2C%20a,been%20removed%20completely%20from%20Quizlet.) by Quizlet in 2023. You can, however, view the script in-action [here](https://www.youtube.com/watch?v=6Z_8w3640I4&ab_channel=wgar).

 This script works by waiting until an asteroid element appears within the DOM, finding its match using the aforementioned dictionary of vocabulary terms, and entering the corresponding text within the input box at the bottom of the screen. At lower levels of the game, the script could eliminate asteroids before they were even visible to the user. 

 The highest achieveable score on Gravity was the 32-bit unsigned integer limit of $`2^{32} - 1`$ or $`4,294,967,295`$. At higher levels, the asteroids moved too fast for human users to be able to achieve a score anywhere near that number, unless they used a flashcard set with [laughably short vocabulary terms, like this user did](https://www.youtube.com/watch?v=tHDpB1PP0kY&t=78s&ab_channel=hyperupcall).

You can see my script reaching this score [in this video](https://www.youtube.com/watch?v=_fPJYLcG208&ab_channel=wgar) with a normal Quizlet set. Note that the game allows you to surpass this score, but it only saves to the leaderboard as the 32-bit unsigned integer limit.

### Match

Match is a Quizlet game that chooses a few random terms from a Quizlet set and lets the user match them within a drag-and-drop environment. This game also contains a leaderboard; however, it ranks the fastest times of completion rather than using a scoring system.

This script works by opening the "micromatch" mode designed for mobile users, which allows for simple successive clicking to match terms rather than dragging-and-dropping. It then finds the tile elements, finds the internal text contained within each one, and clicks on each term followed by its definition using the aforementioned dictionary of vocabulary terms.

It was capable of 1-second completion times, although I could not find a record of its fastest times or videos of it running. 

### Learn

Learn mode consists of a series of multiple-choice and write-in questions. 

The script included within this repository is unfinished, and may not work with current versions of Quizlet since it was last updated in 2020.