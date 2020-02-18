"""
Created on 16 Feb 2020
@author: Milo Bashford

methods for retrieving and sending data to the Team 14 RDS Database
"""

import mysql.connector

from weather import get_weather_data
from weather import flatten_dict


def db_query(**kwargs):

    # dict that associates value of **kwarg["query"] with sql query
    valid_queries = {"push": "INSERT INTO", "pull": "SELECT * FROM", "update": "UPDATE"}

    # dict that associates value of **kwarg["table"] with a valid table name
    valid_tables = {"weather": "dublinbikes.weather_data",
                    "static": "dublinbikes.static_data",
                    "dynamic": "dublinbikes.dynamic_data"}

    # host & login information to database
    host = "dublinbikes.c69eptjjnovd.us-east-1.rds.amazonaws.com"
    passwd = "SET14GP2020"
    user = "admin"

    if "query" in kwargs:
        query = valid_queries[kwargs["query"]]

    if "table" in kwargs:
        table = valid_tables[kwargs["table"]]

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

    print(sql)

    database = mysql.connector.connect(host=host, user=user, passwd=passwd, database="dublinbikes")

    dbcursor = database.cursor(buffered=True)
    dbcursor.execute(sql)

    return dbcursor.fetchall()


# db_query(query="push", table="weather", data=flatten_dict(get_weather_data()))
print(db_query(query="pull", table="dynamic"))
