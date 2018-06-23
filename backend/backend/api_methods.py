from backend.database import get_cursor, aggregate_features, get_stops_for_route, populate_stops, base_url
from backend.fixtures import create_dummy_prediction_fixtures as cdpf
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import ast
import json



def get_predictions_for_route(route="72"):

    route_stops = get_stops_for_route(route=route)

    # testing
    print(len(route_stops))

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

    return delay_list

#@csrf_exempt
def average_delay(delay_list):
        # Im calling this 'delay' for now but what it's really recording is ontimeness
        # To go from native dictionary to JSON, you have to dump to string then load to JSON

        #for testing


        if len(delay_list) != 0:
            avg_delay = abs(sum(delay_list)/len(delay_list))
            avg_delay_dict = json.dumps({"average_delay": avg_delay})
            avg_delay_json = json.loads(avg_delay_dict)

            return avg_delay_json

        else:
            return {"average_delay": None}

#@csrf_exempt
def get_route_line(request, route=72):
        cur = get_cursor()
        cur.execute("SELECT ST_AsGeoJSON(geom :: geometry) FROM mar2512shape WHERE pub_rte='{}'".format(route))
        response = cur.fetchone()[0]
        route_line_json = json.loads(response)
        return route_line_json
