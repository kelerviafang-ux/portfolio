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

| Area | Self Rank | Description |
|---|---:|
| Tools and Equipment Hacks | 3 | Able to open vscode through terminal and commit edited files to Github Actions for a deployed website. |
| Using VS Code | 2 | Knowing what to edit in each file type, such as creating code runners or including important information stored in each file type. |
| GitHub Usage | 3 | How to access issues, project planning in portfolio, pages, and flask. |
| Capstone Project Ideation | 4 | Having a non-profit to help for and ideas on how to improve their website. |

### Tools and Equipment Set Up

Here are key takwaways from what I learned while exploring my tools. 

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
Summary: We picked a new non-profit called My Good Brain that associated with Mental Health, and found specific places in the website to redesign. I focused on the volunteer with MGB tab and here are my ideas: 

- MGB Volunteer tab issues:
1. 3 links directed to the same sign up form
2. Confusing volunteer position info card

- What to improve:
1. Develop database that stores info for all volunteering position and pull from that data base when people are selecting their position
2. Code runner sign ups so people are able to search positions that matches their interest instead of choosing from a list
3. Incorporate if/then statements when sign up of positions contradict. For ex, if someone already signed up for a position that another person wants to sign up, show message such as "unable to sign up"

## Sprint 2

| Area | Self Rank | Description |
|---|---:|
| Lesson Teaching | 3 | Taught detailed lessons so AP CSP students can understand how to use SASS Buttons. |
| HW Hacks | 3 | Was able to do 13 HW Hacks and understanding how each SASS or Python tools work. |
| Frontend & Backend | 2 | Learned how to connect Frontend and Backend through portfolio and flask log in, how to create and kill and server, and API. |
| AP CSP MCQ | 2 | Did a practice test on the actual AP CSP Exam and identified strengths and weakenesses. |

### Sass Buttons Lesson and HW Hacks
Here are brief descriptions on what I did in the lesson and my HW

- SASS Button Lesson: 
1. LxD Cycle (Emphasize, Define, Ideate)
2. College board pseudocode requirements
3. Pairs and teacher feedback

- HW: 
1. All SASS Lessons
2. Python calling procedures, lists, libraries, random values, strings, nested conditions, boolean expression, and developing algorithm

### Frontend, Backend and Data Foundations
Here are new topics that I learned in this lecture: 

- Server Commands:
1. lsof -i :8587 (Search server)
2. kill -9 The 5 digit number showed after running the server (Kill server)
3. python main.py (Run server)

- Backend & Frontend languages 
Frontend: Javascript, HTML, CSS
Backend: API Backend mgb_flask Python, data base SQLite

- API files purpose
1. joke.py: A standard Python file, typically used as the main entry point or a standalone script for an application
2. A pluralized Python module, often used in web frameworks
3. An HTTP request file used by developer tools and extension in VS Code

### AP CSP Practice MCQ
Summary: In My MCQ I mainly got the developing algorithm questions wrong, but I also made errors on other topics such as Identifying and correcting errors, using programs with data, binary numbers, extracting information from data, and fault tolerance

- Developing algorithms:
1. Didn't understand how loop algorithm worked by comparing 2 programs
2. Incorrect on comparing 2 programs, understanding the if/then statement, and predicting how the robot moves or the average of a data set

- Counting binary numbers with our fingers: 
1. Instead of each finger representing 1, each finger represents a power of 2
2. On one hand, the thumb is 1 , index is 2, middle is 4, ring is 8, and pinky is 16. On the other hand, the thumb is 32, index is 64, middle is 128, ring is 256, and pinky is 512. The 2 hands in totle counts to 512. 
3. You can combine 2 or more fingers to create individual numbers such as 3 which is both the thumb and index because 1+2=3. 