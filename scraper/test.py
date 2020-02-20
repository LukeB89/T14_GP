import db_interactions as db
import csv


def main():
    
#   main code which is tasked with running the JSON Parser
#   keeps a log to ensure the returned API information doesnt crash the program.
    dynamic_dict = dict.fromkeys(["number", "last_update", "bike_stands", "available_bike_stands", "available_bikes", "status"], None)
    count = 1
    with open('log.txt', 'a', newline='') as file2:
        out = csv.writer(file2)
        with open('dynamicb.csv', 'r', newline='') as file:
            data = csv.reader(file)
            for line in data:
                if 'number' in line:
                    pass
                else:
                    dynamic_dict["number"] = line[0]
                    dynamic_dict["bike_stands"] = line[1]
                    dynamic_dict["available_bike_stands"] = line[2]
                    dynamic_dict["available_bikes"] = line[3]
                    dynamic_dict["status"] = line[4]
                    dynamic_dict["last_update"] = line[5]
                    out.writerow(count)
                    count += 1
                    db.db_query(query= 'push', table= 'dynamic', data= dynamic_dict )
        
    return
if __name__ == '__main__':
    main()
