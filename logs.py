#!/usr/bin/env python3
# a reporting tool that prints out reports based on the data in the News DB

import psycopg2

DBNAME = "news"


# what are the three most popular articles of all time?
# Ex: 'some popular article title - 1000 views'
def most_popular_articles():
    """
    Find the most popular articles of all time and their number of views
    by running a query that joins the articles and log tables
    """
    conn = psycopg2.connect(database=DBNAME)
    c = conn.cursor()
    c.execute("select title, count(status) as num " +
              "from articles, log " +
              "where concat('/article/', slug) = path and status = '200 OK' " +
              "group by articles.title " +
              "order by num desc limit 3;")
    popular_articles = c.fetchall()
    # print each row of results returned in a more readable format
    for row in popular_articles:
        print(row[0], " - ", row[1], "views")
    print("\n")
    conn.close()


# who are the most popular article authors of all time?
# Ex: Ursula La Multa - 2304 views'
def most_popular_authors():
    """
    Find the most popular authors of all time and their number of views
    by running a query that joins the articles, authors and log tables
    """
    conn = psycopg2.connect(database=DBNAME)
    c = conn.cursor()
    c.execute("select authors.name, count(status) as num " +
              "from articles, authors, log " +
              "where concat('/article/', slug) = path " +
              "and status = '200 OK' " +
              "and articles.author = authors.id " +
              "group by authors.name " +
              "order by num desc;")
    popular_authors = c.fetchall()
    # print each row of results returned in a more readable format
    for row in popular_authors:
        print(row[0], " - ", row[1], "views")
    print("\n")
    conn.close()


# on which day did more than 1% of requests lead to errors?
# Ex: July 29, 2016 - 3.5% errors
# HTTP ERROR STATUS CODES - 404 NOT FOUND
def day_with_erroneous_requests():
    """
    Determine the day on which more than 1 percent of requests were bad
    using two views created in the database (bad_requests and total_requests)
    For the given day, also return the percentage of bad requests.
    """
    conn = psycopg2.connect(database=DBNAME)
    c = conn.cursor()
    c.execute("select to_char(total_requests.day, " +
              "'FMMonth FMDD, YYYY') as day, " +
              "round(bad_requests.requests * 100.0 / " +
              "total_requests.requests, 2) as percent " +
              "from bad_requests, total_requests " +
              "where total_requests.day = bad_requests.day and " +
              "bad_requests.requests * 100 / total_requests.requests > 1.0;")
    bad_days = c.fetchall()
    # print each row of results returned in a more readable format
    for row in bad_days:
        print(row[0], " - ", str(row[1]) + "%")
    conn.close()


print("what are the three most popular articles of all time?")
most_popular_articles()

print("who are the most popular article authors of all time?")
most_popular_authors()

print("On which day did more than 1% of requests lead to errors?")
day_with_erroneous_requests()
