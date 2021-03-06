# Log Analysis

## Description
This program analyzes several tables in a 'news' database and retrieves data to answer these questions:
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

This is the third project of the [Udacity Full Stack Nanodegree Program](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004).

## Instructions
1. Install [VirtualBox](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1) for your operating system.
2. Download and install [Vagrant](https://www.vagrantup.com/downloads.html) for your operating system.
3. Fork and clone this repository.
4. Download the `newsdata.sql` database [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip), unzip it, and place it inside the `vagrant` directory within the `Logs-Analysis-Project-master` folder you just downloaded in step 3.
5. Move the `logs-analyzer.py` file into the same `vagrant` directory as in step 4.
6. Open Terminal (if using a Mac) or Git Bash (if using Windows), and `cd` into the folder called `vagrant` inside of the `Logs-Analysis-Project-master` folder.
7. Run the command `vagrant up` (this may take a few minutes).
8. Once this command is finished running, run the command `vagrant ssh`.
9. Then run the command `psql -d news -f newsdata.sql` to load the data into your local database.
10. Create the 3 `views` listed below in the 'Views' section
11. Quit out of `psql` by running `\q`. You should now be in the `vagrant` directory. From here run the `logs-analyzer.py` file with this command `python logs-analyzer.py`.

## Views

### View 1
```sql
create view total_views as
	select date(time), count(date(time)) as views
	from log
	group by date(time)
	order by date(time);
```

### View 2
```sql
create view status_error as
	select date(time), status, count(date(time)) as num
	from log
	where status like '4%'
	group by date(time), status
	order by date(time);
```

### View 3
```sql
create view error_rate as
	select total_views.date, round((status_error.num::numeric / total_views.views::numeric) * 100, 2) as errors
	from total_views, status_error
	where total_views.date = status_error.date
	order by errors desc;	
```
