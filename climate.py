import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from datetime import datetime, timedelta
import re
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
        f"<h1>Welcome to Hawaii weather analysis!</h1><br />"
        f"Available Routes:<br />"
        f"<ul><li>Precipitation- <code>/api/v1.0/precipitation<code/></li></ul><br/>"
        f"<ul><li>Stations- <code>/api/v1.0/stations<code/></li></ul><br/>"
        f"<ul><li>Temperature- <code>/api/v1.0/tobs<code/></li></ul><br/>"
        f"<ul><li>Trip date- <code>/api/v1.0/<start><code/></li></ul><br/>"
        f"<ul><li>Trip start to end date- <code>/api/v1.0/<start>/<end><code/></li></ul><br/>"
        f"- To get the min, max and average temperature information for your desired trip start date, please use 'Trip date' route. Enter your trip date in YYYY-MM-DD format in link after /. If start date is given the temperatures will be calculated for all dates greater than and equal to the start date.<br/>"
        f"- To get the min, max and average temperature information for your entire trip, please use 'Trip start to end' route. Enter your trip date in YYYY-MM-DD format in link after / . If date range is given the temperatures will be calculatedc for dates between the start and end date inclusive.<br/>"
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
     last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
     last_date = pd.to_datetime(last_date, format='%Y-%m-%d')
     query_date = last_date - timedelta(days=365)
     query_date = query_date.date[0]
     temp = session.query(Measurement.date, Measurement.tobs ).filter(Measurement.date >= query_date).\
        order_by(Measurement.date.desc()).all()

    # Create a dictionary from the row data and append to a list  
     temp_dict = []
     for tobs in temp:
         temperature ={}
         temperature["Temperature"] = tobs
         temp_dict.append(temperature)
     return jsonify(temp_dict)


@app.route("/api/v1.0/<start>")
def start(start):
     session = Session(engine)
     last_date = session.query(Measurement.date,  Measurement.tobs).all()
     
     # Create a dictionary from the row data and append to a list
     all_list = []
     for date, tobs in last_date:
        session_dict ={}
        session_dict["Date"] = date
        session_dict["Temperature"] = tobs
        all_list.append(session_dict)

     for date in all_list:
        search_date = date["Date"]
        if search_date == start:
            temperatures = session.query(func.max(Measurement.tobs), func.avg(Measurement.tobs), func.min(Measurement.tobs)).filter(Measurement.date >= start).all()
           
     
            for max, avg, min in temperatures:
                final_result = {}
                final_result["Maximum Temperature"] = max
                final_result["Average Temperature"] = avg
                final_result["Minimum Temperature"] = min
                return jsonify(final_result)
            
     return jsonify({"error": f"Choose the date range between 2010-01-01 to 2017-08-23 or use YYYY-mm-dd format"}), 404

@app.route("/api/v1.0/<start>/<end>")
def range (start, end):
     session = Session(engine)
     last_date = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
     session.close()
        

     for max, avg, min in last_date:
         range_date = {}
         range_date["Maximum Temperature"] = max
         range_date["Average Temperature"] = avg
         range_date["Minimum Temperature"] = min
         return jsonify(range_date)
        
if __name__ == '__main__':
    app.run(debug=True)
