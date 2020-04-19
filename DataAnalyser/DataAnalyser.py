import json
import os
import sys
import matplotlib.pyplot as plt

file_path = '../Webcrawler/AtiraSpider/spiders/'

# map having tuple (cityname, roomcapacity) as key
city_room_capacity_map = dict()


def does_file_exists(file):
    return os.path.isfile((file_path + file))

def map_city_room_capacity(json):
    for item in jsonData:
        if (item['city'], item['capacity']) in city_room_capacity_map:
            city_room_capacity_map[item['city'], item['capacity']].append(item['price'])
        else:
            city_room_capacity_map[item['city'], item['capacity']] = [item['price']]

def print_avg_price_in_city():
    for k in city_room_capacity_map:
        sumOfList = sum(city_room_capacity_map[k])
        size = len(city_room_capacity_map[k])
        avg = int(sumOfList / size)
        city, capacity = k

        # updating dictionary for further use
        city_room_capacity_map[k] = avg
        print(city +': $'+ str(avg) + ' for ' + str(capacity) + ' person room')

def create_positions(listOfRange):
    listToReturn = []
    position_value = 0
    for n in listOfRange:
        position_value += 5
        listToReturn.append(position_value)
    return listToReturn

def show_bar_chart(data):
    # set figure size
    fig = plt.figure(figsize= (10,100))

    # get x_axis values
    x_axis = list(city_room_capacity_map.keys())

    bar_values = list(city_room_capacity_map.values())

    # get positions on bar graph
    positions = create_positions(list(range(len(list(city_room_capacity_map.keys())))))

    # create bars
    plt.bar(positions, bar_values, width= 0.3)

    # set x-axis
    plt.xticks(positions, x_axis, fontsize = 5)

    # set title
    plt.title('Average price per room capacity in city with tuple (cityName, roomCapacity) on x-axis') 
    plt.show()

if __name__ == '__main__':
    file_name = sys.argv[1]
    if not does_file_exists(file_name):
        print('File does not exist....')
    else:
        # open file
        file = open(file_path + file_name, 'r')

        jsonData = json.load(file)

        # create mapping
        map_city_room_capacity(jsonData)

        # dispaly average price according to room capacity in a city
        print_avg_price_in_city()

        #show bar chart
        show_bar_chart(jsonData)