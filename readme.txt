Projekt Feinstaub


CREATE TABLE SDS011 (
    REF         INTEGER            PRIMARY KEY AUTOINCREMENT,
    sensor_id   INT,
    sensor_type VARCHAR (255),
    timestamp   TIMESTAMP,
    loc_id      INT,
    lon         [DOUBLE PRECISION],
    lat         [DOUBLE PRECISION],
    P1          [DOUBLE PRECISION],
    P2          [DOUBLE PRECISION]
);



CREATE TABLE DHT22 (
    sensor_id    INT,
    sensor_type  VARCHAR (255),
    timestamp    TIMESTAMP,
    loc_id       INT,
    lon          DOUBLE,
    lat          DOUBLE,
    feuchtigkeit DOUBLE,
    [temp]       DOUBLE,
    REF          INTEGER       PRIMARY KEY AUTOINCREMENT
);
