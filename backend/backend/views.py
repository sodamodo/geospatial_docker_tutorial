from backend.database import get_cursor, aggregate_features, get_stops_for_route, populate_stops, base_url
from backend.fixtures import create_dummy_prediction_fixtures as cdpf
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from backend.api_methods import get_predictions_for_route, average_delay, get_route_line
import requests
import ast
import json



@csrf_exempt
def get_route_delay(request, route="72"):

    # The client will supply this with a post request


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



        # isolates route specific predictions
        if type(response) is not dict:
            print("this is the response type-->", type(response))
            continue
        if response.get("RouteName") == route:
            predictions.append(response)


    for prediction in predictions:
        print(prediction.get("PredictedDelayInSeconds"))
        delay_list.append(prediction.get("PredictedDelayInSeconds"))

    print("delay list-->",delay_list)
    print("data type of data list-->", type(delay_list))

    return delay_list
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
    return response

@csrf_exempt
def serve_delay_line_feature(request):
    route="72"

    delay = get_route_delay(request)
    line_json = serve_route_shp_json(request)
    print("where is the data???->", line_json)

    # print("output of get route delay-->", delay)
    print("type of get route delay-->", type(route))
    #
    # print("out put of serve_route_shp_json-->", line_json)
    print("type of serve_route_shp_json-->", type(line_json))



    response = {
                  "type": "Feature",
                  "geometry": {
                    "type": "MultiLineString",
                    "coordinates": {}
                  },
                  "properties": {
                    "route": "",
                    "delay": ""
                  }
                }

    response["geometry"]["coordinates"] = line_json
    response["properties"]["route"] = route
    response["properties"]["delay"] = json.dumps(delay)



    return JsonResponse(response)


#######################################################
#######################################################
#######################################################
#######################################################



@csrf_exempt
def get_avg_delay_for_route(request):


        ##############################################
        # So I don't have to spend all day making calls
        ##############################################
        # with open("72_delay.txt", "r") as f:
        #     response = json.loads(f.read())
        #
        #
        #     return JsonResponse(response)


        # Will receive route from POST from client
        route = "72"

        polyline_json = get_route_line(route)
        delay_list = get_route_delay(route)
        avg_delay = average_delay(delay_list=delay_list)
        print("type of avg delay--->", avg_delay)


        with open('delay_list.txt', 'a+') as outfile:
            outfile.write(str(avg_delay["average_delay"]) + "\n")


        geojson_template = {
                      "type": "Feature",
                      "geometry": {
                        "type": "MultiLineString",
                        "coordinates": ""
                      },
                      "properties": {
                        "route": "",
                        "delay": ""
                      }
                    }


        geojson_template["geometry"]["coordinates"] = polyline_json["coordinates"]
        geojson_template["properties"]["route"] = route
        geojson_template["properties"]["delay"] = avg_delay["average_delay"]

        geojson = geojson_template

        print(geojson)

        with open('72_delay.txt', 'w') as outfile:
            json.dump(geojson, outfile)



        return JsonResponse(geojson)




#######################################################
#######################################################
#######################################################
#######################################################

def get_stored_delay_for_route(request, route="72"):
    cur.execute("SELECT DISTINCT delay FROM route_delays WHERE 'route_name' = {} GROUP BY MAX(time)".format(route))


def populate_routes(request):
    pass


def create_fixtures(request):
        cdpf()

#@csrf_exempt
def get_points(request):

    vehicles_geojson = aggregate_features()
    print("type of data in view-->", vehicles_geojson)
    print("data in view-->", vehicles_geojson)
    return JsonResponse(vehicles_geojson)
