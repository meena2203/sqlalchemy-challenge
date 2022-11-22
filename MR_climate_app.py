# Import dependencies
import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.types import Date
from sqlalchemy.ext.declarative import declarative_base

from flask import Flask, jsonify 
from flask import request

# #################################################
## Database Setup
# create an engine to talk to the database
engine = create_engine('sqlite:///Resources/hawaii.sqlite')

# Reflect an existing database (using automap_base) into a new model
Base = automap_base()

# Use the Base class to reflect the database tables
Base.prepare(engine, reflect=True)

# View all of the classes that automap found
Base.classes.keys()

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# #################################################
# Flask Setup
app = Flask(__name__)


## Flask Routes
# Create and define Homepage route 
@app.route("/")
def Homepage():
    # Welcome and List all available api routes
    return (
        f"Welcome to Hawaii Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>" 
        f"/api/v1.0/<start>/<end>"
     )

# Create and define Precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Design a query to retrieve the last 12 months of precipitation data
    prcp_scores = session.query(measurement.date, measurement.prcp).\
    filter(measurement.date <= '2017-08-23').\
    filter(measurement.date > '2016-08-22').\
    order_by(measurement.date).all()
    prcp_scores

    # Convert the query results to a dictionary using `date` as the key and `prcp` as the value
    prcp_dict = {}
    for date, prcp in prcp_scores:
        prcp_dict[date] = prcp
      
    # Close session
    session.close()

    # Return the JSON representation of your dictionary. 
    return jsonify(prcp_dict)

# Create and define Stations route 
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Design a query to calculate the total number stations in the dataset
    stations = session.query(func.distinct(measurement.station)).all()
    
    # Close session
    session.close()

    # Convert list of tuples into normal list
    stations_list = list(np.ravel(stations))
    
    # Return a JSON list of stations from the dataset.
    return jsonify(stations_list)


# Create and define Temperature observations (tobs) of the most active station route
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Using the most active station id (USC00519281), query the dates and temperature observations of the most active station for the previous year of data.
    active_station_tobs = session.query(measurement.tobs).\
        filter(measurement.date <= '2017-08-23').\
        filter(measurement.date > '2016-08-22').\
        filter_by(station = 'USC00519281').all()
    
    # Close session
    session.close()

    # Convert list of tuples into normal list
    temp_list = list(np.ravel(active_station_tobs))

    # Return a JSON list of tobs of the most active station for the previous year of data.
    return jsonify(temp_list)


# Create and define Temperature statistics route for a given start date
@app.route("/api/v1.0/<start>")
def start_date(start):
    
    # Clean up the user input
    user_input = start.replace("/", "-")
    
    # Create our session (link) from Python to the DB
    session = Session(engine)
  
    # Query - when given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than or equal to the start date OR , or a 404 if not.
    start_query = session.query(func.min(measurement.tobs), 
                                func.avg(measurement.tobs), 
                                func.max(measurement.tobs)).filter(measurement.date >= user_input).all()
    
   # Convert list of tuples into normal list
    result = list(np.ravel(start_query))

    # Return a JSON list of:
    # 'Error' if any of the stats (minimum temperature, the average temperature, and the maximum temperature) is missing for the user input
    # Stats (minimum temperature, the average temperature, and the maximum temperature) for a given start date
    if result[0] == None or result[1] == None or result[2] == None: 
        return jsonify({"error": f"Invalid input, no information is found for your date in the database."}), 404
    else:
        return jsonify({"TMIN": result[0], "TAVG": result[1],"TMAX": result[2]})


# Create and define Temperature statistics route for a given start-end date range
@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    
    # Clean up the user input
    user_input_1 = start.replace("/", "-")
    user_input_2 = end.replace("/", "-")
    
    # Create our session (link) from Python to the DB
    session = Session(engine)
  

    # Query - when given the start and end dates, calculate `TMIN`, `TAVG`, and `TMAX` from the start date through the end date (inclusive), or a 404 if not.
    start_end_query = session.query(func.min(measurement.tobs), 
                                    func.avg(measurement.tobs), 
                                    func.max(measurement.tobs)).filter(measurement.date >= user_input_1).filter(measurement.date <= user_input_2).all()
    
   # Convert list of tuples into normal list
    result = list(np.ravel(start_end_query))

    # Return a JSON list of:
    # 'Error' if any of the stats (minimum temperature, the average temperature, and the maximum temperature) is missing for the user input
    # Stats (minimum temperature, the average temperature, and the maximum temperature) for a given start end date
    if result[0] == None or result[1] == None or result[2] == None: 
        return jsonify({"error": f"Invalid input, no information is found your date range in the database."}), 404
    else:
        return jsonify({"TMIN": result[0], "TAVG": result[1],"TMAX": result[2]})

# Define main behavior
if __name__ == '__main__':
    app.run(debug=True)
