# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import requests
import json

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


    print(stations_id)

def get_sensors_data(id):
    data_request = sensors +str(id)
    print(data_request)
    response = requests.get(data_request)
    data = response.json()
    param_list = []
    param_id = []
    print(data)
    for parameters in range(len(data)):
        param_list.append(data[parameters]['param']['paramName'])
        param_id.append(data[parameters]['id'])
    print(param_id)
    print(param_list)

def get_parameteres_data(id):
    data_request = data_from_sensor + str(id)
    response = requests.get(data_request)
    data = response.json()
    print(data)
    print(data['values'][0]['date'], data['values'][0]['value'])

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # https://powietrze.gios.gov.pl/pjp/content/api
    # get_all_requests('PyCharm') #dva
    # get_request_details(93941) #dva
    # ListaStacji()
    get_sensors_data(291)
    # get_parameteres_data(2039)




# See PyCharm help at https://www.jetbrains.com/help/pycharm/
