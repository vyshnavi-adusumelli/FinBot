# Contributing to TrackMyDollar

Follow the set of guidelines below to contribute to TrackMyDollar!

## Code of Conduct

By participating, you are expected to uphold this code. Please report unacceptable behavior to psomash@ncsu.edu.

Prerequistes required before starting this project

1. Must be a graduate student at NC State University
2. Must be a student in Software Engineering Course in Fall 2021
3. Have proficiency in Python

## How can I Contribute -
 
### Reporting Bugs

This section guides you through submitting a bug report for TrackMyDollar.
Following these guidelines helps maintainers and the community understand your report, reproduce the behavior and find related reports.

Before Submitting A Bug Report

Check the debugging guide

Check the FAQs on the forum for a list of common questions and problems.
Determine which repository the problem should be reported in.

Perform a cursory search to see if the problem has already been reported.

## How Do I Submit A (Good) Bug Report?

Use a clear and descriptive title for the issue to identify the problem.

Describe the exact steps which reproduce the problem in as many details as possible.

Provide specific examples to demonstrate the steps.

Describe the behavior you observed after following the steps and point out what exactly is the problem with that behavior.

Explain which behavior you expected to see instead and why.

Include screenshots and animated GIFs which show you following the described steps and clearly demonstrate the problem.

If the problem is related to performance or memory, include a CPU profile capture with your report.

## Pull Requests

The process described here has several goals:

Maintain the projects quality

Fix problems that are important to users

Enable a sustainable system for the projects maintainers to review contributions

## Tips to Extend

Check the Projects tab for TO-DO list and pick the feature you find interesting to work on.

Create a branch and implement the feature in Python using Telegram bot and test it locally.

Write corresponding test cases to ensure it is not breaking the existing system.

Create pull request and request for the code review. Once the request is approved, merge to main.

Any suggestions to improve the bot is appreciated. Please add it to the TO-DO list.

## More tips for developers
### Heroku deployment
The bot is deployed on [Heroku](https://www.heroku.com/), a website used to host source code and apps.

Quoted directly from their page:

"Heroku is a platform as a service (PaaS) that enables developers to build, run, and operate applications entirely in the cloud."


#### Why this is useful

Before, users had to download source code, insert their API key from telegram, and then run the python file. 
This can lead to both user error and error within the source code. By deploying it on heroku, you ensure that
the code is available anywhere, at anytime, without having to download files.


#### How we created the bot

1. A heroku account was created with the shared mydollarbot@gmail.com credentials
2. A new app was created called my_dollar_bot. 
3. Within github, we added a [new action](.github/workflows/deploy.yml) to deploy to the heroku bot
4. For every push, the source code is deployed to heroku, and python code/bot.py is executed, starting the bot

This way, if users want to use the bot without developing, they can simply use this bot instead of having to run the
application locally.

#### How to develop the heroku bot

- Follow steps 1-3 above, except replace with your own email. Install Heroku cli [here](https://devcenter.heroku.com/articles/heroku-cli#download-and-install).
- Within github, add a secret for the heroku api key
- Create a new CI/CD pipeline (refer our yaml file [here](.github/workflows/deploy.yml)) and set up github actions.
- Within your heroku dashboard, you can view logs for the bot to understand well the deployment is running. You can also run the command `heroku logs` or `heroku logs -t`
