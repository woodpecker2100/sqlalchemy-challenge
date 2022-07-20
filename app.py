#%%

app = Flask(__name__)

engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

measurement = Base.classes.Measurements
station=Base.classes.stations

session = Session(engine)

@app.route("/api/v1.0/precipitation")
def percipitation():
    results = session.query(measurement.date, measurement.prcp).filter(measurement.date >= "2016-08-23").all()
    for item in data:
        data = {}
        data["date"]=measurement.date
        data["prcp"]=measurement.prcp
    return jsonify(data)
@app.route("/api/v1.0/stations")
def stations():
   results = session.query(station.station).all()
   all_names = list(np.ravel(results))
   return jsonify(all_names)
@app.route("/api/v1.0/tobs")
def tobs():
    results = session.query(measurement.tobs).\
    filter(measurement.date >= "2016-08-23").\
    filter(measurement.station == "USC00519281").all()

    temps = list(np.ravel(results))
    return jsonify(temps)
@app.route("/api/v1.0/<start>")
def strtonly(start):
    canonicalized = start.replace(" ", "")
    results = session.query(func.avg(measurement.tobs),func.min(measurement.tobs),func.max(measurement.tobs)).\
    filter(measurement.date >= start).all()
    new_data = list(np.ravel(results))
    return jsonify(new_data)
@app.route("/api/v1.0/<start>/<end>")
def startend(start, end):
    new_start = start.replace(" ", "")
    new_end = end.replace(" ", "")
    results = session.query(func.avg(measurement.tobs),func.min(measurement.tobs),func.max(measurement.tobs)).\
    filter(measurement.date >= start).\
    filter(measurement.date <= end).all()
    new_data = list(np.ravel(results))
    return jsonify(new_data)
if __name__ == "__main__":
    app.run(debug=True)