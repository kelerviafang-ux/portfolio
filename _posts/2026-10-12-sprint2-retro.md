---
toc: True
microblog: True
layout: post
codemirror: True
title: Sprint 2 Retrospective
permalink: /sprint2/retro
author: Kelervia Fang
---
# Sprint 2 Retrospective

## Sprint 1

### Tools and Equipment Set Up
Summary: At the beginning of this course, I learned how to set up and use my tools. The most important tools that I used were terminal and vscode. I learned how to open vscode through terminal by running specific commands. Other commands that I learned were specific the the vscode terminal as I was able to run use them to run the files. I also learned the how to edit files in vscode, and commit the changes to Github Action so we get a delpoyed page of our own code and designs. Lastly, I learned the different files that I used to create specific code runners and include important information.

- How to open vscode through terminal: 
1. Cd (Portfolio, Pages, Flask etc.)
2. ./scripts/venv.sh
3. source venv/bin/activate
4. code .
- VS Code terminal commands:
1. git remote -v (To check what account your in)
2. git pull (To update the changes made on others using the same account)
3. make (Compile project)
- Files and what they're for
1. ipynb (Jupiter Notebook)
2. md (markdown)

### Capstone Project Ideation
Summary: For our capstone project we decided to go with mental health theme as we were all interested in that category. We picked a new non-profit that matched our goal and started looking at their website and identifying places to improve. After finding specific places in the website to redesign we started brainstorming ideas on how to do that. For example, we found out that their dropdown menu was too much as it made it confusing for people to read, so we decided to narrow down the menu in our newly designed website and we incorporated that using specific codes to generate dropdown menu in our deployed website. During the ideation stage, we created a lot of Github issues to desribe what we want to change and improve on the my good brain website. 

- MGB Volunteer tab issues:
1. 3 links directed to the same sign up form
2. Confusing volunteer position info card

- What to improve:
1. Develop database that stores info for all volunteering position and pull from that data base when people are selecting their position
2. Code runner sign ups so people are able to search positions that matches their interest instead of choosing from a list
3. Incorporate if/then statements when sign up of positions contradict. For ex, if someone already signed up for a position that another person wants to sign up, show message such as "unable to sign up"

## Sprint 2

### Sass Buttons Lesson and HW Hacks
Summary: To create the SASS Button lessons, we identified the LxD Cycle (Emphasize, Define, Ideate), college board pseudocode requirements, feedbacks etc. The main goal of the lesson was to teach AP CSP students how to use SASS Buttons to help with their projects. In the Popcorn and HW Hacks we did for other lessons I learned how to create code cells in ipynb files, run them sucessfully in vscode and commit the changes to GitHub Actions for a deployed webpage. After clicking on the localhost link and going into blogs I was able to have a code runner that could run. I also learned how to submit my homework in opencodingsociety and evaluated myself based on how I did in the HW. 

- Important to have In HW
1. Author name on top
2. Description on how code runners work and predicted outcomes

- HW I did
1. All SASS Lessons
2. Python calling procedures, lists, libraries, random values, strings, nested conditions, boolean expression, and developing algorithm

### Frontend, Backend and Data Foundations
Summary: At first we learned how to connect Backend and Frontend through log in systems by using user info from the user management file. We logged in on opencodingsociety in our team portfolio using user: Thomas Edition, and we also logged in out team flask using the same user. Another thing we learned about Backend and Frontend was that Frontend is the actual text that users are able to see and Backend is the data base that we use to store user info. The last thing we learne was API used in Backend where we tested 3 files joke.py, jokes.py, and joke.http with commands that showed specific jokes when we clicked send request. 

- Commands learned:
1. lsof -i :8587 (Search server)
2. kill -9 The 5 digit number showed after running the server (Kill server)
3. python main.py (Run server)

- Backend & Frontend langues 
Frontend: Javascript, HTML, CSS
Backend: API Backend mgb_flask Python, data base SQLite

- Files purpose
1. joke.py: A standard Python file, typically used as the main entry point or a standalone script for an application
2. A pluralized Python module, often used in web frameworks
3. An HTTP request file used by developer tools and extension in VS Code

### AP CSP Practice MCQ
Summary: In My MCQ I mainly got the developing algorithm questions wrong, but I also made errors on other topics such as Identifying and correcting errors, using programs with data, binary numbers, extracting information from data, and fault tolerance

- Developing algorithms:
1. Didn't understand how loop algorithm worked by comparing 2 programs
2. Incorrect on comparing 2 programs, understanding the if/then statement, and predicting how the robot moves or the average of a data set

- Counting binary numbers with our fingers: Instead of each finger representing 1, each finger represents a power of 2. On one hand, the thumb is 1 , index is 2, middle is 4, ring is 8, and pinky is 16. On the other hand, the thumb is 32, index is 64, middle is 128, ring is 256, and pinky is 512. The 2 hands in totle counts to 512. You can combine 2 or more fingers to create individual numbers such as 3 which is both the thumb and index because 1+2=3. 