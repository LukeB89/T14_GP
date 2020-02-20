from sqlalchemy import create_engine

engine = create_engine("mysql://admin:SET14GP2020@dublinbikes.c69eptjjnovd.us-east-1.rds.amazonaws.com:3306/dublinbikes")
engine.connect()

#stands = {}
#dict1 = engine.execute('select number, address from static_data')  # pulling static bike data from DB
#for row in dict1:
#    stands[row['number']] = (row['address'])  # building test dict with the data from DB
#print(stands)

l1 = engine.execute('select name from static_data')
for row in l1:
    print(row['name'])