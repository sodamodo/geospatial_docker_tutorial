from backend.database import get_cursor, aggregate_features, get_stops_for_route, populate_stops, base_url
from backend.fixtures import create_dummy_prediction_fixtures as cdpf
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import ast
import json

@csrf_exempt
def get_points(request):

    vehicles_geojson = aggregate_features()
    print("type of data in view-->", vehicles_geojson)
    print("data in view-->", vehicles_geojson)
    return JsonResponse(vehicles_geojson)

def get_route_delay(request):

    # The client will supply this with a post request
    route="72"

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

        if response.get("RouteName") == route:
            predictions.append(response)


    for prediction in predictions:
        print(prediction.get("PredictedDelayInSeconds"))
        delay_list.append(prediction.get("PredictedDelayInSeconds"))

    # Im calling this 'delay' for now but what it's really recording is ontimeness
    avg_delay = abs(sum(delay_list)/len(delay_list))
    print(json.dumps({"average_delay": avg_delay}))

    return None


def populate_routes(request):
    pass


def create_fixtures(request):
        cdpf()
