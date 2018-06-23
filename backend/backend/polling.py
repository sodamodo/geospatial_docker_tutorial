from database import get_cursor, get_stops_for_route
import datetime
from time import sleep


####################
# poll every 3 hours
###################

cur = get_cursor()

def get_routes():
    cur.execute("SELECT RouteID FROM routes")
    routes = []
    tuple_routes = cur.fetchall()
    [routes.append(tuple_route[0]) for tuple_route in tuple_routes]
    return routes


def get_stops_for_route(route):

    cur.execute("SELECT stopid FROM stoproutes WHERE 'routename' = '{}'".format(route))
    stop_ids = cur.fetchall()
    for stop_id in stop_ids:
        stop_id = (stop_id[0][0])
    return stop_ids

def get_avg_delay_for_route(route="72"):

    route_stops = get_stops_for_route(route=route)

    predictions = []
    delay_list = []
    for stop_id in route_stops:
        r = requests.get(base_url.format("stops/" + stop_id + "/predictions"))
        if r.status_code == 404:
                continue
        response = (ast.literal_eval(r.text)[0])
        response = json.dumps(response)
        response = json.loads(response)

        if type(response) is not dict:
            print("this is the response type-->", type(response))
            continue
        if response.get("RouteName") == route:
            predictions.append(response)


    for prediction in predictions:
        print(prediction.get("PredictedDelayInSeconds"))
        delay_list.append(prediction.get("PredictedDelayInSeconds"))

    sleep(37)

    if len(delay_list) != 0:
        avg_delay = abs(sum(delay_list)/len(delay_list))

        return avg_delay

    else:
        return 0

def store_avg_delay_for_route(route, avg_delay):

    cur.execute("INSERT INTO route_delays (route_name, delay, time) VALUES ('{}', '{}',  '{}')".format(route, avg_delay, datetime.datetime.now()))

route_list = get_routes()

for route in route_list:
    route_avg_delay = get_avg_delay_for_route(route)
    store_avg_delay_for_route(route, route_avg_delay)
    print(route, route_avg_delay)
