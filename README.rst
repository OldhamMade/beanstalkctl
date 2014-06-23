beanstalkctl
============

A shell-like interface for interacting with beanstalkd.

Commands
--------

help
  print the help message

overview
  an overview of the current status

whoami
  Show the current connection details

stats full
  Show all stats for the server
stats short
  Show useful stats for the server
stats tube
  Show stats for a tube

list all
  List all tubes
list buried
  List all tubes with buried jobs
list delayed
  List all tubes with delayed jobs
list ready
  List all tubes with ready jobs
list reserved
  List all tubes with reserved jobs
list urgent
  List all tubes with urgent jobs

put
  put a message onto a queue

peek buried
  Peek at the next buried job on a tube
peek id
  Peek at a specific job using it's id
peek ready
  Peek at the next ready job on a tube

bury one
  bury the next ready job on a tube
bury tube
  bury all jobs on a tube

kick list
  list all tubes with buried jobs
kick one
  kick the next buried job on a tube
kick tube
  kick all buried jobs on a tube
kick everything
  kick all buried jobs from all tubes

delete
  delete a job by ID

clear tube
  clear a tube of all jobs
clear everything
  clear all tubes of all jobs

populate tube
  populate a tube with random jobs
populate tubes
  populate beanstalkd with random tubes and messages
