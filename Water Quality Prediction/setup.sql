drop table predictions
CREATE DATABASE Aqua;

-- Switch to Aqua Database
\c Aqua;

-- Create Table to Store Predictions with Features and Target
CREATE TABLE predictions (
    id SERIAL PRIMARY KEY,
    ph FLOAT,
    iron FLOAT,
    nitrate FLOAT,
    chloride FLOAT,
    lead FLOAT,
    zinc FLOAT,
    color VARCHAR(50),
    turbidity FLOAT,
    fluoride FLOAT,
    copper FLOAT,
    odor VARCHAR(50),
    sulfate FLOAT,
    conductivity FLOAT,
    chlorine FLOAT,
    manganese FLOAT,
    tds FLOAT,
    source VARCHAR(50),
    water_temp FLOAT,
    air_temp FLOAT,
    month INT,
    day INT,
    time_of_day VARCHAR(50),
    prediction int,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


select * from predictions
