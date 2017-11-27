#!/usr/bin/python3

import psycopg2

DBNAME = "news"

# Return the 3 most popular articles in the database, by number of views
find_top_articles = """SELECT title, count(*) AS num
    FROM articles, log
    WHERE log.path = '/article/' || articles.slug
    GROUP BY title
    ORDER BY num DESC
    LIMIT 3;"""

# Return the names of the authors ordered by populariy based on views
find_top_authors = """SELECT name, count(*) AS views
        FROM authors, articles, log
        WHERE authors.id = articles.author
        AND log.path = '/article/' || articles.slug
        GROUP BY name
        ORDER BY views
        DESC;"""

# Return the day(s) and error rate if error requests are greater than 1%
find_high_error_rate = """SELECT to_char(error_rate.date, 'fmMonth DD, YYYY'), error_rate.errors
        FROM error_rate
        WHERE error_rate.errors > 1
        ORDER BY error_rate.errors DESC;"""


def get_db_data(query):
    """Return data from a database query

        Opens a connection with the database, executes the query
        that is passed as an argument, and then returns the query
        results as a list of tuples.

        Args:
            A SQL query. For example:

                SELECT name, id FROM user_database;

        Returns:
            A list of tuples. For example:

                [('DonnyM',32145), ('Sarah',65723), ('Terry',00934)]

    """
    conn = psycopg2.connect(database=DBNAME)
    cur = conn.cursor()
    cur.execute(query)
    return cur.fetchall()
    conn.close()


if __name__ == '__main__':

    # Pass the results of 3 database queries to variables
    articles = get_db_data(find_top_articles)
    authors = get_db_data(find_top_authors)
    errors = get_db_data(find_high_error_rate)

    # Print and format the results of the 3 database querys
    print("\nThe most popular 3 articles of all time:")
    for article in articles:
        print('"' + article[0] + '"', "– " + str(article[1]) + " views")
    print("\nThe most popular authors of all time:")
    for author in authors:
        print(author[0], "– " + str(author[1]) + " views")
    print("\nThe days on which more than 1% of requests led to errors:")
    for error in errors:
            print(error[0], "– " + str(error[1]) + "% errors")
