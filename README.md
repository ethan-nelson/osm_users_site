# OSM Users Site

This group of files creates and runs a database of OpenStreetMap users, their id numbers, and the dates of their first and most recent edits. It also contains a basic website to aid in presenting the information.

## Dependencies

* psycopg2
* [OSM Diff Tool](https://github.com/ethan-nelson/osm_diff_tool)
* [OSM Hall Monitor](https://github.com/ethan-nelson/osm_hall_monitor) (right now, it requires the development version, not the one available from pypi)
* Flask (only if you are interested in a web frontend for searching)

## Included files

The schema of the database is created using `db.sql` for PostgreSQL.

To begin populating the database, `initial_build.py` downloads and reads all the planet diff files. This is a long process and took on the order of one week to complete in October 2015 using a 2.6 GHz processor (one core each for Python and Postgres) with an 8k RPM HDD. The basic idea is that each daily diff file is read and all of the users who submitted a changeset are extracted. With that information, as well as the timestamp of the last edit, we search the database to 1) add them if they are not present in the database or 2) update their latest edit time if they are. If you are a big database guru, this call could likely use some optimization help.

Once you have populated the database with all the daily diff files, you can now run `update.py` to update the database entries every hour as the new hourly diff files are available. This will be your worker process.

`site.py` and `templates/` contain a base Flask framework for a frontend to query the database. This will be your web process. My biggest intention with this project was to allow for wildcard searches to find similarly named accounts, so that is allowed in the database query structure of the website; manually disable this if it's not something you want. The site layout is pretty straightforward, with a home, a POSTable search url, a results page, and an about page. If you are using Apache to serve the website, the `.htaccess` and `osm_users_site.wsgi` files may be of interest to you to place in your `public_html` and `wsgi-bin` directories.

## Troubleshooting

This is a pretty janky workflow put together in two weekends' time...there are likely some issues. It's also heavily custom-built towards my use case. But, I love releasing my code so here it is. 
