# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

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
    """List all available api routes."""
    return (
        f"<strong/>Available Routes:</strong> <br/>"
        f"<br/><strong/>Precipitation from 2016-08-24 to 2017-08-23:</strong> /api/v1.0/precipitation<br/>"
        f"<br/><strong/>Stations:</strong>  /api/v1.0/stations<br/>"
        f"<br/><strong/>TOBs:</strong>  /api/v1.0/tobs<br/>"
        f"<br/><strong/>Temperature for a given start date (use YYYY-MM-DD):</strong>  /api/v1.0/<start><br/>"
        f"<br><strong/>Temperature for a given start and end date (use YYYY-MM-DD):</strong>  /api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all Precipitation Data"""
    # Query all Precipitation
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= "2016-08-24").\
        all()

    session.close()

    # Convert the list to Dictionary
    all_prcp = []
    for date,prcp  in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
               
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all Stations"""
    # Query all Stations
    results = session.query(Station.station).\
                 order_by(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all TOBs"""
    # Query all tobs

    results = session.query(Measurement.date, Measurement.tobs, Measurement.prcp).\
                filter(Measurement.date >= '2016-08-23').\
                filter(Measurement.station=='USC00519281').\
                order_by(Measurement.date).all()

    session.close()

    # Convert the list to Dictionary
    all_tobs = []
    for prcp, date, tobs in results:
        tobs_dict = {}
        tobs_dict["prcp"] = prcp
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>")
def Start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    results = session.query(Measurement.station, Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        group_by(Measurement.date).filter(Measurement.date >= start).group_by(Measurement.date).all()

    session.close()

    # Convert rows to a list of dictionaries
    results_list = []
    for station, date, min_tobs, avg_tobs, max_tobs in results:
        result_dict = {
            'station': station,
            'date': date,
            'min_tobs': min_tobs,
            'avg_tobs': avg_tobs,
            'max_tobs': max_tobs
        }
        results_list.append(result_dict)

    return jsonify(results_list)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start=None, end=None):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    results = session.query(Measurement.station, Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).group_by(Measurement.date).all()

    session.close()

    # Convert rows to a list of dictionaries
    results_list = []
    for station, date, min_tobs, avg_tobs, max_tobs in results:
        result_dict = {
            'station': station,
            'date': date,
            'min_tobs': min_tobs,
            'avg_tobs': avg_tobs,
            'max_tobs': max_tobs
        }
        results_list.append(result_dict)

    return jsonify(results_list)

if __name__ == "__main__":
    app.run(debug=True)

