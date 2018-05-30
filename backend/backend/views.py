from database import get_cursor
from django.http import JsonResponse

def get_points(request):
    cur = get_cursor()

    cur.execute("""
                SELECT json_build_object(
                    'type',       'Feature',
                    'geometry',   ST_AsGeoJSON(the_geom :: geometry) :: json,
                    'properties', json_build_object(
                                  'name', name
                                  )
                    ) jsonb FROM point_table;
                """)

    points = cur.fetchone()

    json_points = points[0]
    return JsonResponse(json_points)
