# Importing dependencies

from flask import Flask, jsonify

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import datetime as dt
import numpy as np
import pandas as pd


# Database Setup

# It doesn't work with "Resources"
engine = create_engine("sqlite:///hawaii.sqlite") 

Base = automap_base()
Base.prepare(engine, reflect=True)
# Base.classes.keys()
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

#FLASK
app = Flask(__name__)


#API specs

@app.route("/api/v1.0/precipitation")
def percipitation():
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= "2016-08-23").all()
    for item in data:
        data = {}
        data["date"]=Measurement.date
        data["prcp"]=Measurement.prcp
    return jsonify(data)


@app.route("/api/v1.0/stations")
def stations():
   results = session.query(Station.station).all()
   all_stations = list(np.ravel(results))
   return jsonify(all_stations)



@app.route("/api/v1.0/tobs")
def tobs():
    results = session.query(Measurement.tobs).\
    filter(Measurement.date >= "2016-08-23").\
    filter(Measurement.station == "USC00519281").all()
    temps = list(np.ravel(results))
    return jsonify(temps)

@app.route("/api/v1.0/<start>")
def strtonly(start):
    canonicalized = start.replace(" ", "")
    results = session.query(func.avg(Measurement.tobs),func.min(Measurement.tobs),func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).all()
    new_data = list(np.ravel(results))
    return jsonify(new_data)

@app.route("/api/v1.0/<start>/<end>")
def startend(start, end):
    new_start = start.replace(" ", "")
    new_end = end.replace(" ", "")
    results = session.query(func.avg(Measurement.tobs),func.min(Measurement.tobs),func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).\
    filter(Measurement.date <= end).all()
    new_data = list(np.ravel(results))
    return jsonify(new_data)
if __name__ == "__main__":
    app.run(debug=True)