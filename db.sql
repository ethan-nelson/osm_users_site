CREATE USER osm_users WITH PASSWORD 'osm';
CREATE TABLE users (userid BIGINT, username TEXT, start_date TIMESTAMP WITHOUT TIME ZONE, end_date TIMESTAMP WITHOUT TIME ZONE);
ALTER TABLE users OWNER TO osm_users;
CREATE TABLE file_list (id SERIAL NOT NULL PRIMARY KEY, sequence TEXT, timestamp TEXT, timetype TEXT, read BOOLEAN);
ALTER TABLE file_list OWNER TO osm_users;
