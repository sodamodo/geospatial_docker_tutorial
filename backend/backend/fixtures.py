import psycopg2
import json
import requests
from time import sleep

from backend.database import get_cursor, aggregate_features, get_stops_for_route, populate_stops, base_url


def create_dummy_prediction_fixtures():
    cur = get_cursor()

    #get list of stops
    cur.execute("SELECT stopId FROM stops;")
    stop_ids_tuples = cur.fetchall()

    # THERE HAS GOT TO BE  A BETTER WAY TO DO THIS
    stop_ids = []
    for stop_id in stop_ids_tuples:
        stop_ids.append(stop_id[0])


    cur.execute("SELECT to_regclass('public.predictions')")
    predictionsExists = cur.fetchone()
    print(predictionsExists[0])

    if predictionsExists[0] != "predictions":
        cur.execute("CREATE TABLE predictions(StopId VARCHAR(5), VehicleId VARCHAR(4), RouteName VARCHAR(5), PredictedDelayInSeconds INT, PredictedDeparture TIMESTAMP,  PredictionDateTime TIMESTAMP)")
        print("table created")


    for stop_id in stop_ids:
        # This is a hacky way to get stop id out of its tuple, look into this later
        # print(base_url.format("stops/" + stop_id[0] + "/predictions"))
        r = requests.get(base_url.format("stops/" + stop_id + "/predictions"))
        sleep(.4
        )
        if r.status_code == 404:
            continue
        predictions = json.loads(r.text)

        for prediction in predictions:
                try:
                    cur.execute("INSERT INTO predictions VALUES ({StopId}, {VehicleId}, '{RouteName}', {PredictedDelayInSeconds}, '{PredictedDeparture}', '{PredictionDateTime}')"
                    .format(StopId=prediction["StopId"], VehicleId=prediction["VehicleId"], RouteName=prediction["RouteName"], PredictedDelayInSeconds=prediction["PredictedDelayInSeconds"], PredictedDeparture=prediction["PredictedDeparture"].replace("T", " "), PredictionDateTime=prediction["PredictionDateTime"].replace("T", " ")))

                # This can probably be done away with once requests
                except TypeError:
                    print("this throws if you have exceeded your 150 reqs/min limit")
                    sleep(60)
