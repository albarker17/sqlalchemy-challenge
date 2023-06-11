# Import the dependencies.

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify



#################################################
# Database Setup
#################################################

engine = create_engine(("sqlite:///Resources/hawaii.sqlite"))

# reflect an existing database into a new model

Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement

station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    return(
        f"Aloha! Hawaii Climate HomePage - Available Routes:<br/>"
        f"Percipitation Data: <b/r>"
        f"/api/v1.0/precipitation<br/>"
        f"Active Weather Stations: <b/r>"
        f"/api/v1.0/stations<br/>"
        f"Temp Observations: <b/r>"
        f"/api/v1.0/tobs<br/>"
        f"<b/r>"
        f"/api/v1.0/<start><br/>"
        f"<b/r>"
        f"/api/v1.0/<start>/<end>"

    )
#route for percipitation
@app.route("/api/v1.0/precipitation")
def percipitation():

    session=Session(engine)

    one_year = dt.date(2017,8,23) - dt.timedelta(days = 365)

    results = session.query(measurement.date, measurement.prcp).filter(measurement.date >= one_year).all()
    

    percip = []
    for date, prcp in results:
        percip_dict = {}
        percip_dict["date"] = prcp
        percip.append(percip_dict)
    return jsonify(percip)

#route for stations

@app.route("/api/v1.0/stations")
def stations():

    session=Session(engine)

    results = session.query(station.name).all()

    session.close()

    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

#tobs route

@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(engine)

    one_year = dt.date(2017,8,23) - dt.timedelta(days = 365)

    most_active = session.query(measurement.date, measurement.tobs).filter(measurement.station =='USC00519281').filter(measurement.date >= one_year).all()

    session.close()

    most_active_station = []
    for date, temp in most_active:
        most_active_dict = {}
        most_active_dict[date] = temp
        most_active_station.append(most_active_dict)

    return jsonify(most_active_station)

#start date route for 06.24.2016
@app.route("/api/v1.0/<start>")


def start(start):

    session = Session(engine)

    start_date = '2016-06-24'

    start_results = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).filter(measurement.date >= start_date).all()
    

    #close session

    session.close()

    start_d = []
    for min, max, avg in start_results:
        start_dictionary = {}
        start_dictionary["Min Temp"] = min
        start_dictionary["Max Temp"] = max
        start_dictionary["Avg Temp"] = avg
        start_d.append(start_dictionary)


        return jsonify(start_d)
    
# route for start date of 06.24.2016 and end date of 08.20.2016
@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start,end):

    session = Session(engine)

    start_date = '2016-06-24'

    end_date = '2016-08-20'

    start_end_results = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).filter(measurement.date>= start_date).filter(measurement.date <= end_date).all()
    
    session.close()

    start_end_d = []
    for min, max, avg in start_end_results:
        start_end_dictionary = {}
        start_end_dictionary["Min Temp"] = min
        start_end_dictionary["Max Temp"] = max
        start_end_dictionary["Avg Temp"] = avg
        start_end_d.append(start_end_dictionary)


    return jsonify(start_end_d)


if __name__ == "__main__":
    app.run(debug = True)


