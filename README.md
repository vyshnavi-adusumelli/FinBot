# TrackMyDollar
<hr>
<p align="center">
<a><img width=500 
  src="https://github.com/deekay2310/MyDollarBot/blob/c56b4afd4fd5bbfffea0d0a4aade58596a5cb678/docs/0001-8711513694_20210926_212845_0000.png" alt="Expense tracking made easy!"></a>
</p>
<hr>

![MIT license](https://img.shields.io/badge/License-MIT-green.svg)
![GitHub](https://img.shields.io/badge/Language-Python-blue.svg)
![GitHub contributors](https://img.shields.io/github/contributors/mtkumar123/MyDollarBot)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5590961.svg)](https://doi.org/10.5281/zenodo.5590961)
[![Platform](https://img.shields.io/badge/Platform-Telegram-blue)](https://desktop.telegram.org/)
[![Build Status](https://app.travis-ci.com/mtkumar123/MyDollarBot.svg?branch=main)](https://app.travis-ci.com/mtkumar123/MyDollarBot)
[![codecov](https://codecov.io/gh/mtkumar123/MyDollarBot/branch/main/graph/badge.svg?token=W50WL3ZLMC)](https://codecov.io/gh/mtkumar123/MyDollarBot)
![GitHub issues](https://img.shields.io/github/issues-raw/mtkumar123/MyDollarBot)
![GitHub closed issues](https://img.shields.io/github/issues-closed-raw/mtkumar123/MyDollarBot)

<hr>

## About TrackMyDollar

TrackMyDollar is an easy-to-use Telegram Bot that assists you in recording your daily expenses on a local system without any hassle.  
With simple commands, this bot allows you to:
- Add/Record a new spending
- Show the sum of your expenditure for the current day/month
- Display your spending history
- Clear/Erase all your records
- Edit/Change any spending details if you wish to

---

<p align="center"><img width="1000" src="./docs/workflows/add.gif"></p>

---

## Table of contents

- [TrackMyDollar](#trackmydollar)
  * [About TrackMyDollar](#about-trackmydollar)
- [:star: Whats New](#star-whats-new)
- [:rocket: Installation Guide](#rocket-installation-guide)
- [:information_desk_person: Samples](#information_desk_person-samples)
    + [Budget](#budget)
    + [Add](#add)
    + [Delete](#delete)
    + [Edit](#edit)
- [:grey_question: Documentation](#grey_question-documentation)
- [:raising_hand: Team Members](#raising_hand-team-members)
- [:calling: Support](#calling-support)



# :star: Whats New

### Version 1.0.1

#### New Features:

- Users are now able to upload a csv file containing transactions with columns “Date”, “Description”,  “Debit”, and “Date. The bot will go through each transaction in the csv file, and for transactions it has already seen before, the bot will automatically classify that transaction into the right category. For transactions, that the bot has not seen before, the bot will request the user to choose the appropriate category for that transaction.
- Consistent input and output format for all date values, and numeric values of transactions

#### For Contributors:

- Test cases have been completely written. Test cases in the bot folder are tests for functions in the bot.py, while test cases in the unit folder are for the user.py.
- Updated the documentation for all functions.
- Updated Readme.md to reflect current team working on this project.

### Version 1.0.0

#### New Features:

- Users are now able to set a budget expenditure for each category. If users exceed the budget for that category, a message it displayed reminding the user of the budget they had initially set. 
- Users are now able to delete their entire transaction history, or choose to delete just one transaction

#### For Contributors:

- Code has been refactored, and split into two main python files. Bot.py handles all the bot processing functions, and interacts with the bot handler directly. User.py handles all the backend User processing logic, and creates an object User for each individual user interacting with the bot, to maintain that user’s state. 
- Data is stored within the user object, and state is saved using a pickle object. 
- Created CI pipeline using Travis CI, and pylint to check for formatting errors, and code coverage to test for code coverage. 


<!-- [comment]: <> (## Demo) -->

<!-- [comment]: <> (https://user-images.githubusercontent.com/15325746/135395315-e234dc5e-d891-470a-b3f4-04aa1d11ed45.mp4) -->



# :rocket: Installation Guide


1. Install Python, atleast Python3

2. Clone this repository to your local system at a suitable directory/location of your choice

3. Start a terminal session, and navigate to the directory where the repo has been cloned

4. Run the following command to install the required dependencies:
```
  pip install -r requirements.txt
```
5. Download and install the Telegram desktop application for your system from the following site: https://desktop.telegram.org/

6. Once you login to your Telegram account, search for "BotFather" in Telegram. Click on "Start" --> enter the following command:
```
  /newbot
```
7. Follow the instructions on screen and choose a name for your bot. Post this, select a username for your bot that ends with "bot" (as per the instructions on your Telegram screen)

8. BotFather will now confirm the creation of your bot and provide a TOKEN to access the HTTP API - copy this token for future use.

9. In the directory where this repo has been cloned, navigate to the "code" folder and open the "code.py" file. This file consists of a variable by the name "api_token". Paste the token copied in step 8 in the placeholder provided for this variable:
```
  api_token = "INSERT API KEY HERE"
```
10. In the Telegram app, search for your newly created bot by entering the username and open the same. Once this is done, go back to the terminal session. Navigate to the directory containing the "code.py" file and run the following command:
```
  python bot/code.py
```
11. A successful run will generate a message on your terminal that says "TeleBot: Started polling." 
12. Post this, navigate to your bot on Telegram, enter the "/start" or "/menu" command, and you are all set to track your expenses!



# :information_desk_person: Samples

### Budget

I want to increase/decrease my monthly budget.

<p align="center"><img width="700" src="./docs/workflows/budget.gif"></p>

1. Enter the `/budget` command
2. Enter the new budget amount (must be greater than 0)


### Add

I just spent money and want to mark it as a transaction! 

<p align="center"><img width="700" src="./docs/workflows/add.gif"></p>

1. Enter the `/add` command
2. Click on the date of the transaction
3. Click on the category to add
4. Type in the amount spent

### Delete

Oh no! I entered a transaction but want to delete it! 

<p align="center"><img width="700" src="./docs/workflows/delete.gif"></p>

1. Enter the `/delete` command
2. Based on how many records you want to delete..
   1. Per day: enter the day to delete
   2. Per month: enter the month to delete
   3. All: enter All
3. The records will be display. Enter YES to confirm, or NO to cancel

### Edit

Oh no! I entered a transaction but entered the wrong category! 

<p align="center"><img width="700" src="./docs/workflows/edit.gif"></p>

1. Enter the `/edit` command
2. Specify the date, category, and value of the transaction
3. Specify what part of the transaction to edit (either date, category, or value)
4. Enter in a new value

## Adding transactions from CSV and displaying chart

I want to add transactions from a CSV my bank gave me, and visalize my spendings

<p align="center"><img width="700" src="./docs/workflows/csv_vis.gif"></p>


1. Drag the .csv file into the telegram chat, and press send
2. For each transaction, classify the category
   1. The application will remember these mappings
3. Enter the `/chat` command


# :grey_question: Documentation


Thorough documentation of all methods and classes can be found HERE



# :raising_hand: Team Members

## Version 1.0.0
- Ashley King
- Manoj Kumar
- Rakesh Muppala
- Sayali Parab
- Ashwin Das
- Renji Joseph Sabu

## Version 1.0

### Team Members
- Dev 
- Prakruthi 
- Radhika
- Rohan
- Sunidhi


# :calling: Support

For any support, email us at mydollarbot@gmail.com
