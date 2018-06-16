import psycopg2
import json
import requests
import ast

base_url = "https://api.actransit.org/transit/{}/?token=369BB8F6542E51FF57BC06577AFE829C"

def get_cursor():
    conn = psycopg2.connect(dbname="gis", user="gisuser", password="password", host="localhost")
    conn.autocommit = True
    cursor = conn.cursor()
    return cursor

def make_vehicle_point(vehicleid):
    cur = get_cursor()
    sql_string = ("""
                SELECT json_build_object(
                    'type',       'Feature',
                    'geometry',   ST_AsGeoJSON(location :: geometry) :: json,
                    'properties', json_build_object(
                                  'vehicle', {0}
                                  )
                    ) jsonb FROM vehicles WHERE vehicleid={0};
                """).format(str(vehicleid))

    cur.execute(sql_string)
    points = cur.fetchall()

    json_points = points[0][0]

    return json_points

def aggregate_features():
    ####
    # This will be more than one element. This will get each feature using the
    #list of vehicle IDs. There will be a call for each vehicle to them make into feature
    # as feature objects
    ####

    feature_collection = {"type": "FeatureCollection", "features": [] }
    cur = get_cursor()

    cur.execute("SELECT vehicleid FROM vehicles LIMIT 2")
    vehicle_tuples = cur.fetchall()

    vehicles = []
    for vehicle in vehicle_tuples:
        vehicles.append(vehicle[0])

    #now pass each vehicle id to the function
    for vehicle in vehicles:

        # Accepts integer as parameter, returns dict
        vehicle_feature = make_vehicle_point(vehicle)
        feature_collection["features"].append(vehicle_feature)

    # Is this necessary?
    feature_collection = json.dumps(feature_collection)
    feature_collection = json.loads(feature_collection)

    return feature_collection

def get_stops_for_route(route):

    base_url = "https://api.actransit.org/transit/{}/?token=369BB8F6542E51FF57BC06577AFE829C"
    cur = get_cursor()

    #get list of stops for route parameter
    cur.execute("SELECT stopid FROM stoproutes WHERE routename='{}';".format(route))
    print("SELECT stopid FROM stoproutes WHERE routename='{}';".format(route))
    stop_ids_tuples = cur.fetchall()

    # THERE HAS GOT TO BE  A BETTER WAY TO DO THIS
    stop_ids = []
    for stop_id in stop_ids_tuples:
        stop_ids.append(stop_id[0])


    return stop_ids




    # print(base_url.format("stops/37.8044/122.2711/500/" + route))
    # r = requests.get(base_url.format("37.8044/122.2711/105600/" + route))
    # print(r.text)


def populate_stops():

    base_url = "https://api.actransit.org/transit/{}/?token=369BB8F6542E51FF57BC06577AFE829C"
    cur = get_cursor()

    # cur.execute("DROP TABLE IF EXISTS stops ;")

    # Checks to see if it's been prefilled

    cur.execute("SELECT to_regclass('public.stops')")
    tableExists = cur.fetchone()
    if tableExists[0] != "stops":
        cur.execute("CREATE TABLE stops(stopId VARCHAR(5), name VARCHAR(100), geo GEOGRAPHY(POINT));")

        print("stops table doesn't exist")
        r = requests.get(base_url.format("stops"))
        stops = json.loads(r.text)
        for n in stops:
            stop_id = str(n["StopId"])
            name = n["Name"].replace("'","")
            lat = n["Latitude"]
            long = n["Longitude"]

            insert_string = "INSERT INTO stops (stopID, name, geo) VALUES({stop_id}, '{name}', ST_SetSRID(ST_MakePoint({long}, {lat}), 4326))".format(stop_id=stop_id, name=name, long=long, lat=lat)

            cur.execute(insert_string)
            cur.execute("SELECT * FROM stops;")


        print("stops populated")
