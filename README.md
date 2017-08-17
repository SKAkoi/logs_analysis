# Logs Analysis Project
--------------------------------------------

## Intro
This project uses Python's DB-API to build a reporting tool that uses information
from a database to analyse the webserver log for a news website.

## Setting up
1. Install [Python](https://www.python.org)
2. Install [Virtual Box](https://www.virtualbox.org/wiki/Downloads)
3. Install and set up [Vagrant](https://www.vagrantup.com/downloads.html)
4. Start up the Virtual Machine after configuring Vagrant

## Getting the data
1. Download the data from [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)
2. Unzip the downloaded file for a file called newsdata.sql
3. Put newsdata.sql into the vagrant folder
4. Fire up the VM using ```vagrant ssh```
5. Load the site's data into your local database using the command
```psql -d news -f newsdata.sql
```


## Running queries
1. Run ```psql news```
2. Create the following views in the database for later use by logs.py when it's
running:

 A view for the number of bad requests each day
```sql
create view bad_requests
    as select date(time) as day, count(status) as requests
    from log where status != '200 ok'
    group by day
    order by requests desc;
```

A view for the number of total requests each day
```sql
create view total_requests
    as select date(time) as day, count(status) as requests
    from log
    group by day
    order by requests desc;
```
3. Run logs.py to see the result of the queries
