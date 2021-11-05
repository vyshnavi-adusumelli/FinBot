| Score | Self-Assessment | Notes | Evidence |
| --- | --- | ---- | ------ |
|.5| .5 |short release cycles| We have a total of 4 releases. https://github.com/mtkumar123/MyDollarBot/releases|
|.5| .5 | workload is spread over the whole team (so one team member is often Xtimes more productive than the others...| Everyone contributed and had commits. Can be seen in insights https://github.com/mtkumar123/MyDollarBot/graphs/contributors?from=2021-10-01&to=2021-11-01&type=c|
|.5| .5 |Docs: why: docs tell a story, motivate the whole thing, deliver a punchline that makes you want to rush out and use the thing | readme.md on main sells our project very well. https://github.com/mtkumar123/MyDollarBot/blob/main/README.md|
|.5| .5 |the files CONTRIBUTING.md lists coding standards and lots of tips on how to extend the system without screwing things up  | contributing.md is very detailed https://github.com/mtkumar123/MyDollarBot/blob/main/CONTRIBUTING.md|
|.5| .5 |Docs: doco generated , format not ugly  | Github pages https://mtkumar123.github.io/MyDollarBot/|
|.5| .5 | evidence that the whole team is using the same tools (e.g. config files in the repo, updated by lots of different people) | Everyone has a working instance of the project locally. All the team members are using the same IDE and have all the required packages installed. The whole team uses the same testing telegram bot. This can be seen within our github secrets, as API_TOKEN is set to the shared API_TOKEN all team members share.|
|.5| .5 | evidence that the members of the team are working across multiple places in the code base | We assign issues in Github and start working on the required part of the project. The commit history of different members shows this. https://github.com/mtkumar123/MyDollarBot/graphs/contributors?from=2021-10-01&to=2021-11-04&type=c|
|1| 1 |Docs: what: point descriptions of each class/function (in isolation)  | Each function has a docstring, and is used to generate the documentation for github pages using sphinx|
|.5| .5 | Number of commits: by different people  | Insights https://github.com/mtkumar123/MyDollarBot/graphs/contributors?from=2021-10-01&to=2021-11-04&type=c|
|1| 1 |issues are being closed | 27 issues were opened and closed https://github.com/mtkumar123/MyDollarBot/issues|
|.5| .5 | issues are discussed before they are closed | Example https://github.com/mtkumar123/MyDollarBot/issues/61 |
|.5| .5 | Use of syntax checkers. | Used pylint, and have a pylintrc file |
|1| 1 | Issues reports: there are many  | https://github.com/mtkumar123/MyDollarBot/issues?q=is%3Aissue+is%3Aclosed|
|.5| .5 | Use of code formatters. | pylint, and used pylintrc for config of pylint also used black formatter and added the badge in the repo |
|.5| .5 | Use of style checkers | pylint, and used pylintrc for config of pylint |
|.5| .5 | Docs: short video, animated, hosted on your repo. That convinces people why they want to work on your code. | Multiple gifs found in the readme.md https://github.com/mtkumar123/MyDollarBot/blob/main/README.md|
|.5| .5 | test cases exist  | all test cases in the test folder. code coverage is 68 percent |
|.5| .5 | Use of code coverage  | codecov.yml file, and code coverage is 68%|
|.5| .5 | other automated analysis tools  | Pylint, CodeCoverage, Github Actions, Pytest. |
|.5| .5 |test cases:.a large proportion of the issues related to handling failing cases. | When a test failed, an issue was opened tagged as bug. Example https://github.com/mtkumar123/MyDollarBot/issues/23|
|.5| .5 |test cases are routinely executed | github actions to run the tests routinely. build badge to show the build is passing |
|1| 1 |Documentation describing how this version improves on the older version| What's New Section in the readme.md https://github.com/mtkumar123/MyDollarBot/blob/main/README.md|
|3| 3 | This version is a little(1), some(2), much(3) improved on the last version.|Tutor's assessment.| 
