# Bridges

A bridge serves as a platform for two-way communication. Here, I've documented such `bridges` used in this repository.

### Configuration details

Following is a list of software's used in this repository.

- Database: MySQL Workbench - `version 8.0`
- Programming language: Python 3 - `version 3.7.7`
- Programming IDE: Spyder 3 

### MySQL connector for python 3

I'm using `sqlalchemy` library, to communicate between MySQL and python.  

- In Python 3, install the `sqlalchemy` library as, 
	- `> pip install SQLAlchemy`
- Create a mysql engine to establish connection between python and mysql, like, 	
	- `engine = sqlalchemy.create_engine('mysql://user:password@server') # connect to server`
	- mysql engine [configuration help](https://docs.sqlalchemy.org/en/13/core/engines.html)
- Write a python pandas dataframe to mysql by using the `to_sql()` function. --
	- `pandas_dataframe.to_sql(name='mysql_table_name', con=mysql_engine, if_exists='replace')`
