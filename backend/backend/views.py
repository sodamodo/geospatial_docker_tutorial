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

@csrf_exempt
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



        print("Routename type-->", type(response.get("RouteName")))

        if type(response) == "dict":
            if response.get("RouteName") == route:
                predictions.append(response)
    

    for prediction in predictions:
        print(prediction.get("PredictedDelayInSeconds"))
        delay_list.append(prediction.get("PredictedDelayInSeconds"))

    # Im calling this 'delay' for now but what it's really recording is ontimeness
    # To go from native dictionary to JSON, you have to dump to string then load to JSON
    avg_delay = abs(sum(delay_list)/len(delay_list))
    avg_delay_dict = json.dumps({"average_delay": avg_delay})
    avg_delay_json = json.loads(avg_delay_dict)

    return JsonResponse(avg_delay_json)

#####
# Split get_route_delay into 2 functions, one will just return route
# supplied by client post request so that it can be passed to both get_route_delay
# serve_delay_line_feature
##### (supplied)
@csrf_exempt
def serve_route_shp_json(request):
    route="72"

    cur = get_cursor()
    cur.execute("SELECT ST_AsGeoJSON(geom :: geometry) FROM mar2512shape WHERE pub_rte='{}'".format(route))
    response = cur.fetchone()[0]
    response = json.loads(response)

    return JsonResponse(response)

def serve_delay_line_feature(request):
    route="72"
    print(get_route_delay(request))

    response = """
                        {
                      "type": "Feature",
                      "geometry": {
                        "type": "MultiLineString",
                        "coordinates": {cordinates}
                      },
                      "properties": {
                        "name": {route},
                        "delay": {delay}
                      }
                    }
                        """.format(delay=get_route_delay(request), coordinates=serve_route_shp_json(request))

    return JsonResponse(json.loads(response))

def populate_routes(request):
    pass


def create_fixtures(request):
        cdpf()
