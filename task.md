# Tessian QA Engineer take home test
You are given a bot that was built a long time ago, and never deployed. 
The team would like to get it working and make changes that make this chatbot scalable in production, 
as it will be deployed in a high traffic environment.

## Part 1 : Code Review
Pretend you are seeing `bot.py` on a github PR, and submitting your code review of this code.
Make a list of things that should be improved in this code before putting this bot into production.
Feel free to also include any review comments related to software engineering best practices.
Note that you do not need to implement these changes!

## Part 2 : Bug
This bot had a test (in `test.py`), which is currently failing.
We know the test is correct and the problem lies in the application code, so please explain the reason for the failure and suggest a fix.

## Part 3 : Testing
The existing test coverage is unfortunately lacking, so please add any tests you feel are missing to `test.py` (to be super clear, please do add your own test code containing any missing test coverage).
Additionally, for any testing that would need more context or internal knowledge, feel free to speculate on what kinds of tests you would propose adding, given the deployment scenario
this bot will be in. You may make assumptions wherever needed regarding architecture, platform or deployment details, please state any assumptions made as well.