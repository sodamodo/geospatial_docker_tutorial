import psycopg2

def get_cursor():
    conn = psycopg2.connect(dbname="gis", user="gisuser", password="password", host="localhost")
    cursor = conn.cursor()
    return cursor
