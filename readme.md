chorebot
========

chorebot helps with the tedious parts of organizing household chores using
Trello. 

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

* Deployment - build virtualenv and get the code there

https://hynek.me/talks/python-deployments/
http://dan.bravender.net/2012/5/11/git-based_fabric_deploys_are_awesome.html

* Daemonize the application using... what? 
  upstart is not recommended? Scary warning if you try to install it.
  systemd?
  http://supervisord.org/index.html

