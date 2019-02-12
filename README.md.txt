# Logs Analysis Project

1. What are the most popular three articles of all time?
  Which articles have been accessed the most?
  Present this information as a sorted list with the most popular article at the top
2. Who are the most popular article authors of all time?
  That is, when you sum up all of the articles each author has written, which authors get the most page views?
  Present this as a sorted list with the most popular author at the top.
3. On which days did more than 1% of requests lead to errors?
  The log table includes a column status that indicates the HTTP status code that the news site sent to the user's browser.

## Requirements
* Python 3.7
* psycopg3
* Postgresql 9.6

## How to run
* install Python from link
https://www.python.org/downloads/

* install VirtualBox from link
https://www.virtualbox.org/wiki/Downloads

* install Vagrant from link
https://www.vagrantup.com/downloads.html

* get the news database from link
https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip

* bring the virtual mahine online, run the command
```
vagrant up
```
* log into vagrant, run dhe command
```
vagrant ssh
```
* load the data onto the database
```sql
psql -d news -f newsdata.sql
```
* connect to the database
```sql
psql -d news
```
* create views
* python3 LogsAnalysis.py

### Create Views
```sql
create view authors_articles 
as select name, slug, title 
from authors join articles
on authors.id = articles.author;
```

```sql
create view path_slug 
as select title, status 
from articles, log 
where split_part(log.path,'/',3) = articles.slug;
```

```sql
create view date_view 
as select date(time), COUNT(*) 
as views from log 
group by date(time)
orde by date(time);
```

```sql
create view date_error 
as select date(time), COUNT(*) as errors 
from log WHERE status = '404 NOT FOUND' 
group by date(time) 
order by date(time);
```

```sql
create view views_rate 
as select date_view.date, 
(100.0 date_error.errors/date_view.views) as percentage
from date_view, date_error
where date_view.date = date_view.date
order by date_view.date;
```

### select query
```sql
select title, count(*) as titles_views from path_slug 
where status = '200 OK' 
group by title
order by titles_views desc 
limit 3;
```
```sql
select name, count(*) as authors_views from authors_articles 
join path_slug on path_slug.title = authors_articles.title
group by name
order by authors_views desc;
```
```sql
select * from views_rate where percentage > 1 
order by percentage desc;
```

