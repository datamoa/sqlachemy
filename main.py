import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#Database setup
engine =create_engine('sqlite:///Resources/hawaii.sqlite')

# reflect an existing database into a new model
Base = automap_base()
#reflect the tables
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

app= Flask(__name__)

@app.route("/")
def index():
    return (
        f"Welcome to Home page!<br />"
        f"Available Routes:<br />"
        f"/api/v1.0/precipitation<br />"
        f"/api/v1.0/stations<br />"
        f"/api/v1.0/tobs<br />"
        f"/api/v1.0/<br />"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;<br />"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
     """Return a list of percipitatipn data """
     #Query all prcp data
     session = Session(engine)
     results = session.query(Measurement.date, Measurement.prcp).all()

     # Create a dictionary from the row data and append to a list
     precipitation = []
     for date, prcp in results:
         precipitation_dict ={}
         precipitation_dict["Date"] = date
         precipitation_dict["Precipitation"] = prcp
         precipitation.append(precipitation_dict)
     return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def stations():
    #Query stations list from dataset
     session = Session(engine)
     names = session.query(Measurement.station).group_by(Measurement.station).all()

    # Create a dictionary from the row data and append to a list
     stat_names = []
     for station in names:
         stat_dict ={}
         stat_dict["Station"] = station
         stat_names.append(stat_dict)
     return jsonify(stat_names)

@app.route("/api/v1.0/tobs")
def tobs():
     session = Session(engine)
     temp = session.query(Measurement.date, Measurement.tobs ).filter(Measurement.date >= '2016-08-23').\
        order_by(Measurement.date.desc()).all()

     temp_dict = []
     for tobs in temp:
         temperature ={}
         temperature["Temperature"] = tobs
         temp_dict.append(temperature)
     return jsonify(temp_dict)

@app.route("/api/v1.0/<start>")
def user_input(start):
     session = Session(engine)
     max_temp = [func.max(Measurement.tobs),
           func.min(Measurement.tobs),
           func.avg(Measurement.tobs)]
     stat_data = session.query(*max_temp).\
         filter(Measurement.date >= start).all()
     #return jsonify ("Max Temp " + stat_data[0] + "Min Temp " +  stat_data[1] + "AVG Temp" + stat_data[2])
     return jsonify(stat_data)
    #  statistics = []
    #  for stat in stat_data:
    #      day_stat ={}
    #      day_stat ['Max Temp'] = func.max(Measurement.tobs)
    #      day_stat ['Min Temp'] = func.min(Measurement.tobs)
    #      day_stat ['AVG Temp'] = func.avg(Measurement.tobs)
    #      statistics.append(day_stat)
    #  return (statistics)
    


if __name__ == '__main__':
    app.run(debug=True)
