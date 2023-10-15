# :money_with_wings: SlashBot
<hr>
<p align="center">
<a><img width=500 
  src="/docs/workflows/banner.jpg" alt="Expense tracking made easy!"></a>
</p>
<hr>

![MIT license](https://img.shields.io/badge/License-MIT-green.svg)
![GitHub](https://img.shields.io/github/languages/top/vyshnavi-adusumelli/FinBot?color=red&label=Python&logo=Python&logoColor=yellow)
![GitHub contributors](https://img.shields.io/github/contributors/vyshnavi-adusumelli/FinBot)
[![DOI](https://zenodo.org/badge/431190543.svg)](https://zenodo.org/badge/latestdoi/431190543)
[![Platform](https://img.shields.io/badge/Platform-Telegram-blue)](https://desktop.telegram.org/)
[![codecov](https://codecov.io/gh/vyshnavi-adusumelli/FinBot/branch/main/graph/badge.svg?token=YCKWZTHO7O)](https://app.codecov.io/gh/vyshnavi-adusumelli/FinBot/)
[![Actions Status](https://github.com/vyshnavi-adusumelli/FinBot/workflows/CI/badge.svg)](https://github.com/vyshnavi-adusumelli/FinBot/actions)
![github workflow](https://github.com/vyshnavi-adusumelli/FinBot/actions/workflows/black.yml/badge.svg)
![Discord](https://img.shields.io/discord/879343473940107264?color=blueviolet&label=Discord%20Discussion%20Chat)
![Lines of code](https://img.shields.io/tokei/lines/:provider/:user/https%3A%2F%2Fgithub.com%2Fvyshnavi-adusumelli%2FFinBot)
![Version](https://img.shields.io/github/v/release/vyshnavi-adusumelli/FinBot?color=ff69b4&label=Version)
![GitHub issues](https://img.shields.io/github/issues-raw/vyshnavi-adusumelli/FinBot)
![GitHub closed issues](https://img.shields.io/github/issues-closed-raw/vyshnavi-adusumelli/FinBot)

<hr>

## Demo Video

https://youtu.be/NBihyIU13pw

## About SlashBot

SlashBot is an easy-to-use Telegram Bot that assists you in recording your daily expenses on a local system without any hassle.  
With simple commands, this bot allows you to:
- Add/Record a new spending
- Show the sum of your expenditure for the current day/month
- Display your spending history
- Clear/Erase all your records
- Edit/Change any spending details if you wish to
- Download your expenditure history in the CSV format
- Visualize your spendings in the form of graphs/pie chart using the /chart option
- Email the history CSV file to yourself
- See the total daily/monthly expenditure in different currencies

Check out the bot here: https://t.me/ncsuBot

---
Sample demos are shown below. They are run on a local machine.

- [:information_desk_person: Sample Demos](#information_desk_person-Sample-Demos)


---

# :star: Whats New

### Release Version 1.2.1

- See your total daily/monthly expenditure in differet currencies using the /displayDifferentCurrency command
- Download your spendings history CSV file using the /download command
- Email the monthly spendings history to yourself using the /sendEmail command
- User can now get a message when the monthly budget is exhausted.
- Details for testing requirements added in README.md


### Release Version 1.2.0

- Visualize your spendings in the form of graphs
- The User can now see his expenses across various categories in the form of graphs along with pie charts.
- Just go on adding multiple spendings using /add and type /chart to see the spendings in the form of graphs.
- More Badges added in Repository




<!-- [comment]: <> (## Demo) -->

<!-- [comment]: <> (https://user-images.githubusercontent.com/15325746/135395315-e234dc5e-d891-470a-b3f4-04aa1d11ed45.mp4) -->



# :rocket: Installation Guide

## 💻For developers 
1. Install Python, atleast Python3

2. Clone this repository to your local system at a suitable directory/location of your choice

3. Start a terminal session, and navigate to the directory where the repo has been cloned

4. Run the following command to install the required dependencies:
```
  pip install -r requirements.txt
```
5. Ensure that you export the PYTHONPATH variable to the main project folder in the environment variables. This is essential for your Python scripts to locate and import the project modules correctly.

### Telegram Installation

### Discord Installation

### Testing with Pytest

1. Ensure that all necessary environment variables are correctly set on your computer. These variables are crucial for the functioning of your bot and test environment:

DISCORD_TOKEN: Your Discord bot's token.
CHANNEL_ID: The ID of the Discord channel your bot operates in.
API_TOKEN: The API token for your Telegram bot.
CHAT_ID: The ID of the chat where your Telegram bot operates.
PYTHONPATH: Set the PYTHONPATH variable to the main project folder. This helps your Python scripts locate and import project modules correctly.

2. Navigate to the FinBot/test/unit folder in your project directory. In your terminal, run the following command:
```
  python -m pytest
```
After running the tests, you should see a summary indicating the number of test failures and passes.

# :information_desk_person: Sample Demos

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

### Adding transactions from CSV and displaying chart

I want to add transactions from a CSV my bank gave me, and visalize my spendings

<p align="center"><img width="700" src="./docs/workflows/csv_vis.gif"></p>


1. Drag the .csv file into the telegram chat, and press send
2. For each transaction, classify the category
   1. The application will remember these mappings
3. Enter the `/chart` command

### Download History

I want a CSV file of all my transactions.

<p align="center"><img width="700" src="./docs/workflows/download.gif"></p>

1. Make sure you have a transaction history.
2. Enter the `/download` command.
3. A CSV file will be sent with your history.

### See total Expenditure in different currencies

I want to convert my total daily or monthly expenditure in a different currency.

<p align="center"><img width="700" src="./docs/workflows/currencyWorking.gif"></p>

1. Enter the /displayDifferentCurrency command
2. Choose from the category of day or month
3. Next, Choose your currency from the options
4. You will get the converted price in that currency


### Visualization in the form of graphs

I want to see my spendings in the form of graphs

<p align="center"><img width="700" src="./docs/workflows/multipleVisualizations.gif"></p>

1. Make sure you have a transaction history.
2. Enter the `/chart` command.
3. You will see multiple visualizations for your spending 

### SendEmail 

I want to send myself an email for the monthly expenditure


<p align="center"><img width="700" src="./docs/workflows/email.gif"></p>

1. Make sure you have a transaction history.
2. Enter the `/sendEmail` command.
3. Type the intended email address
4. You will get an email with the history file as attachment

# :grey_question: Documentation

Thorough documentation of all methods and classes can be found at [Github Pages](https://mtkumar123.github.io/MyDollarBot/)

# :construction: Road Map

Our ideas for new features that can be implemented to make this project better can be seen in our RoadMap project board.
[Road Map](https://github.com/secheaper/slashbot/projects/1)



:heart: Acknowledgements
---
We would like to thank Dr. Timothy Menzies for helping us understand the process of building a good Software Engineering project. We would also like to thank the teaching assistants Xiao Ling, Andre Lustosa, Kewen Peng, Weichen Shi for their support throughout the project.


:page_facing_up: License
---
This project is licensed under the terms of the MIT license. Please check [License](https://github.com/secheaper/slashbot/blob/main/LICENSE) for more details.


:sparkles: Contributors
---

<table>
  <tr>
    <td align="center"><a href="http://www.shubhammankar.com/"><img src="https://avatars.githubusercontent.com/u/29366125?v=4" width="75px;" alt=""/><br /><sub><b>Shubham Mankar</b></sub></a></td>
    <td align="center"><a href="https://github.com/pratikdevnani"><img src="https://avatars.githubusercontent.com/u/43350493?v=4" width="75px;" alt=""/><br /><sub><b>Pratik Devnani</b></sub></a><br /></td>
    <td align="center"><a href="https://github.com/moksh98"><img src="https://avatars.githubusercontent.com/u/29693765?v=4" width="75px;" alt=""/><br /><sub><b>Moksh Jain</b></sub></a><br /></td>
    <td align="center"><a href="https://rahilsarvaiya.tech/"><img src="https://avatars0.githubusercontent.com/u/32304956?v=4" width="75px;" alt=""/><br /><sub><b>Rahil Sarvaiya</b></sub></a><br /></td>
    <td align="center"><a href="https://github.com/annie0467"><img src="https://avatars.githubusercontent.com/u/17164255?v=4" width="75px;" alt=""/><br /><sub><b>Anushi Keswani</b></sub></a><br /></td>
  </tr>
</table>



# :calling: Support

For any support, email us at mydollarbot@gmail.com/ secheaper@gmail.com
