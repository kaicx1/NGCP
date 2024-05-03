import time
import csv

def read_csv_live(live_file):
    lat_coors_list = []
    long_coors_list = []
    bearing_list = []
    highest_percentage = -1
    while True:
        try:
            with open(live_file,'r') as file:
                csv_reader = csv.reader(file)
                accuracyIndex = 0
                index = 0
                for row in csv_reader:
                    lat_coors_list.append(float(row[8]))  # Convert to float directly
                    long_coors_list.append(float(row[9]))  # Convert to float directly
                    # Determine bearing
                    i = 17
                    power = 0
                    bearing_degree = float(row[1])

                    while i < 377:
                        if float(row[i]) > power:
                            power = float(row[i])
                            bearing_degree = (bearing_degree - 90 - (i-17)) % 360
                        i = i + 1

                    bearing_list.append(bearing_degree)

                    # Store highest value in highest_percentage
                    if float(row[2]) > highest_percentage:
                        highest_percentage = float(row[2])
                        accuracyIndex = index
                    index = index + 1

                return lat_coors_list, long_coors_list, bearing_list, accuracyIndex
        except Exception as e:
            print("Error:", e)
