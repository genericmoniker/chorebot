chorebot
========

chorebot helps with the tedious parts of organizing household chores using
Trello as the user interface and data store.

Use Trello to create the chores that you want, and chorebot will assign them 
out at an appropriate frequency.
 
Gamification of chore completion is planned.

**WARNING**: Very early development!


Setup
-----

Chorebot depends on Python 2.7.

After cloning the chorebot source, you can optionally create and activate a 
virtual environment. Install the dependencies with:

    pip install -r requirements.txt

Chorebot can be set up to run nightly using cron or some other scheduling
mechanism that your OS supports. Simply invoke main.py.


Trello Board Setup
------------------

Create a board that has "Chores" in the name.

Create a holding list for chores. This could be called "Done", but it doesn't
really matter.

Create a list for each person to be assigned chores. The list should include 
the person's first name according to their Trello account, as well as "To Do"
or "ToDo". For example: "Eric - To Do".

Create cards for all your chores. Use labels to indicate how often the chore
should be done. Supported label names are:

* Daily
* Twice weekly
* Weekly
* Monthly

If you want a chore to go to a specific person every time or shuffled among a 
group of people every time, add the "members" to that card.

Cards without members will be shuffled and dealt among all the to do lists.

Note: When looking for boards, lists, cards and members, chorebot searches 
case-insensitively, so for example, your board could be "Smithy family chores",
and your to do list "eric-todo" and those will work just fine.


Keys and Tokens
---------------

Get an API key and secret at 
[https://trello.com/app-key](https://trello.com/app-key).

Follow the directions for getting an OAuth token and secret at
[https://github.com/sarumont/py-trello](https://github.com/sarumont/py-trello).

All of these need to be saved in config.ini.


To Do
-----

* Email on error (or create a card?)
* Optimal retrieval from server (esp. Card.fetch)
* Fail in an obvious way if config.ini isn't set up
* Optionally get board name from config.ini (also for testing).
