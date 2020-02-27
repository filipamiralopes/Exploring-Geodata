import pandas as pd
import gmplot  # https://github.com/vgm64/gmplot
import os

API_KEY = os.getenv("API_KEY") #google maps api key (environment variable)

def get_merge_files():

    files = ['00.csv', '01.csv', '02.csv', '03.csv', '04.csv', '05.csv', '06.csv', '07.csv', '08.csv',
             '09.csv', '10.csv', '11.csv', '12.csv', '13.csv', '14.csv']

    dfs = [pd.read_csv('events_treated/' + x) for x in files]
    all_events = pd.concat(dfs)

    all_events=all_events.drop(columns='Unnamed: 0')

    return all_events

def separate_imsis(all_events):

    imsi_1 = all_events.loc[(all_events.imsi_sha256 == '0df96b53e1bd1b4cd1377ce2dcf7f12bb9384f915e2f12d1bbc4e5e5b2668b90')]
    imsi_2 = all_events.loc[(all_events.imsi_sha256 == '7a3751d3534bd8e50e69afc6a1d3e40b5d14fc33b12333dc7649a05ad224971c')]
    imsi_3 = all_events.loc[(all_events.imsi_sha256 == '149394f92c7b6e07d66c792a68b0f232064fe9eff5d873da1486e81280592a48')]
    imsi_4 = all_events.loc[(all_events.imsi_sha256 == 'ce9e62301ddce626128b708220d2498d34c38f0ceac753de4836b426a0747a29')]

    return(imsi_1, imsi_2, imsi_3, imsi_4)

def add_marker_and_line(my_map, imsi):

    latitude_list = imsi['latitude']
    longitude_list = imsi['longitude']
    first_latitude = imsi.iloc[0][4]
    first_longitude = imsi.iloc[0][5]
    last_latitude = imsi.iloc[-1][4]
    last_longitude = imsi.iloc[-1][5]

    my_map.marker(first_latitude, first_longitude, 'red', title='first signal')
    my_map.marker(last_latitude, last_longitude, 'blue', title='last signal')
    my_map.scatter(latitude_list, longitude_list, '#000000', size = 15, marker = False)
    my_map.plot(latitude_list, longitude_list, color='black', edge_width = 2.5)

def draw_map(imsi_1, imsi_2, imsi_3, imsi_4):

    my_map = gmplot.GoogleMapPlotter(50.86, 9.63, 6, apikey=API_KEY)

    add_marker_and_line(my_map, imsi_1)
    add_marker_and_line(my_map, imsi_2)
    add_marker_and_line(my_map, imsi_3)
    add_marker_and_line(my_map, imsi_4)

    my_map.draw('my_maps/my_map.html')

def main(): #call all functions

    all_events = get_merge_files()
    [imsi_1, imsi_2, imsi_3, imsi_4] = separate_imsis(all_events)
    draw_map(imsi_1, imsi_2, imsi_3, imsi_4)

if __name__=='__main__':
    main()
