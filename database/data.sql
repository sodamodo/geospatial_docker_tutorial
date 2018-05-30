CREATE TABLE IF NOT EXISTS point_table (the_geom GEOMETRY(POINT, 3857), name VARCHAR(12));
INSERT INTO point_table(the_geom, name) VALUES(ST_GeomFromText('POINT(-122.156830 37.725685)', 3857), 'Oakland');

