# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import requests
import json
import plotly.graph_objects as go

#wgr api key 745637C5-C372-472B-8F0D-29E16B3074E9
#key = '745637C5-C372-472B-8F0D-29E16B3074E9'
tech_key = '&TECHNICIAN_KEY=29992A0F-7D93-4461-A561-33889A8B0BD0&format=json'
stacje = 'https://api.gios.gov.pl/pjp-api/rest/station/findAll'
sensors = 'https://api.gios.gov.pl/pjp-api/rest/station/sensors/'
data_from_sensor = 'https://api.gios.gov.pl/pjp-api/rest/data/getData/'
def get_request_details(request_id):
    url = 'http://dkvdc-sdwl0001.dovista.org:/sdpapi/request/93941'
    print("url =", url)
    parameters = '&OPERATION_NAME=GET_REQUEST_FIELDS'
    input_data = """{
        "operation": {
            "details": {
            "from": "0",
            "limit": "500",
            "filterby": "Product Support_QUEUE"
            }
        }
    }"""
    request_details = requests.get(url +
                            parameters +
                            tech_key)
    data = request_details.text
    print("request details:", request_details.text)
    pass

def get_all_requests(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
    url = 'http://dkvdc-sdwl0001.dovista.org:/sdpapi/request?INPUT_DATA='
    parameters = '&OPERATION_NAME=GET_REQUESTS'
    input_data = """{
    "operation": {
        "details": {
            "from": "0",
            "limit": "5",
            "filterby": "All_Completed"
            "requesttemplate": 
        }
    }
}"""
    # "filterby": "Product Support_QUEUE"
    response = requests.get(url +
                            str(input_data) +
                            parameters +
                            tech_key)
    # print('Response from OPC: ',response.json())
    data = response.json()

    request_id = data['operation']['details'][0]['WORKORDERID']
    print("items in: ",len(data['operation']['details']))
    # overdue = 0
    # for x in range(0,len(data['operation']['details'])):
    #     print("test2 :", data['operation']['details'][x]['WORKORDERID'],data['operation']['details'][x]['SUBJECT'],data['operation']['details'][x]['ISOVERDUE'])
    #     if data['operation']['details'][x]['ISOVERDUE'] == "true" \
    #             and data['operation']['details'][x]['REQUESTTEMPLATE'] == "Exemption - ROSIE":
    #         overdue += 1
    # print("overdue = ", overdue)
    print('Some tests: ',data)


def ListaStacji():
    response = requests.get(stacje)
    data = response.json()
    stations_names = []
    stations_id = []
    stations_longitude = []
    stations_latitude = []
    print(data[0]['stationName'])
    for station in range(len(data)):
        stations_names.append(data[station]['stationName'])
        stations_id.append(data[station]['id'])
        stations_latitude.append(data[station]['gegrLat'])
        stations_longitude.append(data[station]['gegrLon'])

    parameters_texts = []

    for id in stations_id:
        parameters_text = get_sensors_data(id)
        parameters_texts.append(parameters_text)
    print(parameters_texts[0])

    # create_Map(stations_latitude,stations_longitude,stations_names, parameters_texts)

def get_sensors_data(id):
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
        text = text + f'{param_list[item]} : \t {measurement_values[item]} pomiar o: \t {measurement_times[item]}\n'
    # print(f'ID stacji: {id}\n{text}')
    return text

def get_parameteres_data(id):
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
    return measurement_time,  measurement_value

def create_Map(latitude_list, longitude_list, name_list, text_list):
    # Use a breakpoint in the code line below to debug your script.

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

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # https://powietrze.gios.gov.pl/pjp/content/api
    # get_all_requests('PyCharm') #dva
    # get_request_details(93941) #dva
    ListaStacji()
    # get_sensors_data(291)
    # get_parameteres_data(10120)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
