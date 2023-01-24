# imports
import requests
import json
import plotly.graph_objects as go
import time

# hardcoding
# links
# official gov site with API resources: https://powietrze.gios.gov.pl/pjp/content/api
stacje = 'https://api.gios.gov.pl/pjp-api/rest/station/findAll'
sensors = 'https://api.gios.gov.pl/pjp-api/rest/station/sensors/'
data_from_sensor = 'https://api.gios.gov.pl/pjp-api/rest/data/getData/'

def ListaStacji():
    print('script start')
    start = time.time()
    response = requests.get(stacje)
    data = response.json()
    print('json acquired')
    stations_names = []
    stations_id = []
    stations_longitude = []
    stations_latitude = []
    
    for station in range(len(data)):
        stations_names.append(data[station]['stationName'])
        stations_id.append(data[station]['id'])
        stations_latitude.append(data[station]['gegrLat'])
        stations_longitude.append(data[station]['gegrLon'])

    print('stations data added')
    print(f'It took {round((time.time() - start),2)}')
    parameters_texts = []

    for id in stations_id:
        start = time.time()
        parameters_text = get_sensors_data(id)
        parameters_texts.append(parameters_text)
        print(f'data for sensor id:{id} \t taken. It took {round((time.time() - start),2)}')
    print('sensors data acquired')
    #return parameters_texts

    create_Map(stations_latitude,stations_longitude,stations_names, parameters_texts)

def get_sensors_data(id):
    start = time.time()
    data_request = sensors +str(id)
    response = requests.get(data_request)
    data = response.json()
    param_list = []
    param_id = []

    for parameters in range(len(data)):
        param_list.append(data[parameters]['param']['paramName'])
        param_id.append(data[parameters]['id'])

    measurement_values = []
    measurement_times = []
    for id in param_id:
        measurement_time, measurement_value = get_parameteres_data(id)
        measurement_values.append(measurement_value)
        measurement_times.append(measurement_time)

    text = ""
    for item in range(len(param_list)):
        text = text  + f'{param_list[item]} : \t {measurement_values[item]} pomiar o: \t {measurement_times[item]}<br>'
    # print(f'ID stacji: {id}\n{text}')
    print(f'get sensor data took {round((time.time() - start),2)}')
    return text

def get_parameteres_data(id):
    start = time.time()
    data_request = data_from_sensor + str(id)

    response = requests.get(data_request)
    data = response.json()
    # print(data)
    try:
        measurement_time = data['values'][0]['date']
    except TypeError:
        measurement_time = 'n/a'
    except IndexError:
        measurement_time = 'n/a'
    try:
        measurement_value = data['values'][0]['value']
    except TypeError:
        measurement_value = 'n/a'
    except IndexError:
        measurement_value = 'n/a'

    # print(measurement_value, measurement_time)
    print(f'get parameters data took {round((time.time() - start),2)}')
    return measurement_time,  measurement_value

def create_Map(latitude_list, longitude_list, name_list, text_list):
    # function to create map with stations and info hovering on them

    mapbox_access_token = open(".mapbox_token").read()
    # https://stackoverflow.com/questions/42753745/how-can-i-parse-geojson-with-python

    fig = go.Figure()

    fig.add_trace(go.Scattermapbox(
        lat=latitude_list,
        lon=longitude_list,
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=17,
            color='rgb(255, 0 , 0)',
            opacity=0.7
        ),
        text=name_list,
        hoverinfo='text'
    ))

    fig.add_trace(go.Scattermapbox(
        lat=latitude_list,
        lon=longitude_list,
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=8,
            color='rgb(242, 177, 172)',
            opacity=0.7
        ),
        text=text_list,
        hoverinfo='text'
    ))

    fig.update_layout(
        title='Stacje pogodowe',
        autosize=True,
        hovermode='closest',
        showlegend=True,
        mapbox=dict(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=dict(
                lat=53,
                lon=-8
            ),
            pitch=0,
            zoom=3,
            style='light'
        ),
    )
    fig.show()

if __name__ == '__main__':
    
    ListaStacji()

    #just some testing
    # get_sensors_data(291)
    # get_parameteres_data(10120)

