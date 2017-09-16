#!/usr/bin/env python3
# a reporting tool that prints out reports based on the data in the News DB

import sys
import psycopg2


def connect(db_name = "news"):
    """
    Connects to the PostgreSQL database and returns the cursor and db variables
    """
    try:
        db = psycopg2.connect(database="news")
        c = db.cursor()
        return db, c
    except psycopg2.Error as e:
        """
        If connecting to the database fails, print a message and exit Program
        """
        print("Unable to make database connection. Program exiting")
        sys.exit(1)


def fetch_query(query):
    """
    Connects to the database, query, fetch results, close connection, return
    results
    """
    db, c = connect()
    c.execute(query)
    results = c.fetchall()
    db.close()
    return results

def most_popular_articles():
    """
    Fetch the most popular articles using the fetch_query helper function and
    print the results
    """
    print("What are the most popular articles of all time?")
    results = fetch_query("select title, count(status) as num " +
              "from articles, log " +
              "where concat('/article/', slug) = path and status = '200 OK' " +
              "group by articles.title " +
              "order by num desc limit 3;")
    for row in results:
        print(row[0], " - ", row[1], "views")
    print("\n")

def most_popular_authors():
    """
    Fetch the most popular authors using the fetch_query helper function and
    print the results
    """
    print("What are the most popular authors of all time?")
    results = fetch_query("select authors.name, count(status) as num " +
              "from articles, authors, log " +
              "where concat('/article/', slug) = path " +
              "and status = '200 OK' " +
              "and articles.author = authors.id " +
              "group by authors.name " +
              "order by num desc;")
    for row in results:
        print(row[0], " - ", row[1], "views")
    print("\n")

def most_error_days():
    """
    Fetch the days with more than 1% of bad requests and print the
    results
    """
    print("On which day did more than 1% of requests lead to errors?")
    results = fetch_query("select to_char(total_requests.day, " +
              "'FMMonth FMDD, YYYY') as day, " +
              "round(bad_requests.requests * 100.0 / " +
              "total_requests.requests, 2) as percent " +
              "from bad_requests, total_requests " +
              "where total_requests.day = bad_requests.day and " +
              "bad_requests.requests * 100 / total_requests.requests > 1.0;")
    for row in results:
        print(row[0], " - ", str(row[1]) + "%")

if __name__ == '__main__':
    most_popular_articles()
    most_popular_authors()
    most_error_days()
