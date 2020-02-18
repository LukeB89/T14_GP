"""
Created on 16 Feb 2020
@author: Milo Bashford

methods for retrieving and sending data to the Team 14 RDS Database
"""

import mysql.connector
import traceback


def db_query(**kwargs):
    """Constructs & sends a query to the RDS database

    Takes **kwargs: 'query', 'table', 'data'. """

    # dict that associates value of **kwarg["query"] with sql query
    valid_queries = {"push": "INSERT INTO", "pull": "SELECT * FROM", "update": "UPDATE"}

    # dict that associates passed **kwarg["table"] with a valid table
    valid_tables = {"weather": "dublinbikes.weather_data",
                    "static": "dublinbikes.static_data",
                    "dynamic": "dublinbikes.dynamic_data"}

    # host & login information to database
    host = "dublinbikes.c69eptjjnovd.us-east-1.rds.amazonaws.com"
    passwd = "SET14GP2020"
    user = "admin"
    database = "dublinbikes"

    # establish connection to database
    connection = mysql.connector.connect(host=host, user=user, passwd=passwd, database=database)

    # construct the sql query from the passed arguments
    if "query" in kwargs:
        query = valid_queries[kwargs["query"]]
    else:
        return "Error: no such query: " + kwargs["query"]

    if "table" in kwargs:
        table = valid_tables[kwargs["table"]]
    else:
        return "Error: no such table: " + kwargs["table"]

    if "data" in kwargs:
        data = kwargs["data"]
        values = []
        fields = ""
        fields_type = ""

        for key in data:
            if len(fields) < 1:
                fields += key
                fields_type += "%s"
            else:
                fields += ", " + key
                fields_type += ", %s"

            values.append(str(data[key]))

        sql = query + " " + table + " (" + fields + ") VALUES (" + fields_type + ")"

    else:
        sql = query + " " + table

    # execute the sql query
    try:
        dbcursor = connection.cursor(buffered=True)

        # on insert query
        if kwargs["query"] == "push":
            dbcursor.execute(sql, values)
            connection.commit()

        # on update query
        elif kwargs["query"] == "update":
            dbcursor.execute(sql)
            connection.commit()

        # on select query
        elif kwargs["query"] == "pull":
            dbcursor.execute(sql)
            return dbcursor.fetchall()

        # query not defined
        else:
            print("Error: query not defined")
            return False
    except:
        print(traceback.format_exc())
        return False


# db_query(query="push", table="weather", data=flatten_dict(get_weather_data()))
# sample_data = {'number': 249, 'contract_name': 'dublin', 'name': 'SMITHFIELD NORTH', 'address': 'Smithfield North', 'lat': 53.349562, 'lng': -6.278198}
# print(db_query(query="pull", table="static"))
