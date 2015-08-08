chorebot
========

chorebot helps with the tedious parts of organizing household chores using
Trello.


Trello Board Setup
------------------

Create a board that has "Chores" in the name.

Create a holding list for chores. This could be called "Done", but it doesn't
really matter.

Create a list for each person to be assigned chores. The list should include 
the person's first name according to their Trello account, as well as "To Do"
or "ToDo". For example: "Eric - To Do".

Create cards for all your chores. Use labels to indicate how often the chore
should be done:

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

Deployment
----------

You can use [supervisord](http://supervisord.org/index.html) to manage the
process.

Copy the project files to the host. Restart the process with:
supervisorctl restart chorebot


To Do
-----

* Email on error (or create a card?)

* Optimal retrieval from server (esp. Card.fetch)

* Deployment - build virtualenv and get the code there

https://hynek.me/talks/python-deployments/
http://dan.bravender.net/2012/5/11/git-based_fabric_deploys_are_awesome.html

* Daemonize the application using... what? 
  upstart is not recommended? Scary warning if you try to install it.
  systemd?
  http://supervisord.org/index.html

