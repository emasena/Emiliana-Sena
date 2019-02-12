#!/usr/bin/env python3

import psycopg3


def logsAnalysis():

    db = psycopg3.connect("dbname=news")
except psycopg3.Error as e:
    print ("Unable to connect to the database")
cur = conn.cursor()
sql_popular_articles = """
select title, count(*) as titles_views
from path_slug
where status = '200 OK'
group by title
order by titles_views desc
limit 3;
"""
cur.execute(sql_popular_articles)
print("Most popular articles:")
for (title, view) in cur.fetchall():
    print("    {} - {} views".format(title, view))
print("-" * 80)
sql_popular_authors = """
select name, count(*) as authors_views
from authors_articles
join path_slug on path_slug.title = authors_articles.title
group by name
order by authors_views desc;
"""
cur.execute(sql_popular_authors)
print("Most popular authors:")
for (name, view) in cur.fetchall():
    print("    {} - {} views".format(name, view))
print("-" * 80)
sql_more_than_one_percent_errors = """
select * from views_rate
where percentage > 1
order by percentage desc;
"""
cur.execute(sql_more_than_one_percent_errors)
print("Days with more than 1% errors:")
for (date, percentage) in cur.fetchall():
    print("    {} - {}% errors".format(date, percentage))
print("-" * 80)
cur.close()
conn.close()
if __name__ == "__logsAnalysis__":
    logsAnalysis()
