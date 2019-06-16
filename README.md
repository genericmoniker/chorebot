chorebot
========

[![Build
Status](https://travis-ci.org/genericmoniker/chorebot.svg?branch=master)](https://travis-ci.org/genericmoniker/chorebot)


chorebot helps with the tedious parts of organizing household chores 
using Trello as the user interface and data store.

Use Trello to create the chores that you want, and chorebot will assign 
them out at an appropriate frequency.
 
Gamification of chore completion is planned.

**WARNING**: Very early development!


Setup
-----

Chorebot depends on Python 3.6+ and is managed with
[Poetry](https://poetry.eustace.io/).

Chorebot can be set up to run nightly using cron or some other 
scheduling mechanism that your OS supports. Simply invoke main.py.


Using Docker
------------

Chorebot can run as a Docker container.

    $ docker build -t chorebot .
    $ docker run -t --rm -v ${CONFIG_DIR}:/config --name chorebot-cont chorebot

Where `${CONFIG_DIR}` would be replaced by the path to a directory that
contains your config.ini file (see Configuration below).


Trello Board Setup
------------------

Create a board that has "Chores" in the name.

Create a holding list for chores. This could be called "Done", but it 
doesn't really matter.

Create a list for each person to be assigned chores. The list should 
include the person's first name according to their Trello account, as 
well as "To Do" or "ToDo". For example: "Eric - To Do".

Create cards for all your chores. Use labels to indicate how often the 
chore should be done. Supported label names are:

* Daily
* Twice weekly
* Weekly
* Monthly

If you want a chore to go to a specific person every time or shuffled 
among a group of people every time, add the "members" to that card.

Cards without members will be shuffled and dealt among all the to do 
lists.

Note: When looking for boards, lists, cards and members, chorebot 
searches case-insensitively, so for example, your board could be "Smith 
family chores", and your to do list "eric-todo" and those will work just 
fine.


Configuration
-------------

Get an API key at: 
[https://trello.com/app-key](https://trello.com/app-key)

Also, generate a token on the same page by clicking the appropriate link
there.

These need to be saved in config.ini, which should be either in the 
project root directory or `/config/config.ini`.

    [Auth]
    api_key: <your API key goes here>
    token: <your token goes here>
    
You can also customize which board chorebot will use: 
    
    [App]
    chore_board: housework


To Do
-----

* Implement "Monthly" chores
* Create a card logger so that logs can be read with Trello
* Fail in an obvious way if config.ini isn't set up
* Integration tests with a test board
* Unit tests for gamify.py
