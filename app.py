
# Python SQL toolkit and Object Relational Mapper
from pickletools import StackObject
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import datetime as dt
import pandas as pd
import numpy as np

from flask import Flask, jsonify
# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Declare a Base using `automap_base()`
Base = automap_base()


# Use the Base class to reflect the database tables
Base.prepare(engine, reflect=True)

# Print all of the classes mapped to the Base
Base.classes.keys()

# Assign the Measurement/station classes to a variable called `Demographics`
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session
session = Session(engine)



app = Flask(__name__)


############# Hello Route ############
@app.route('/')
def hello():
    return 'Hello World!'

#############WELCOME route ##############
@app.route('/Welcome')
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!\n
    Available Routes:\n
    /api/v1.0/precipitation\n
    /api/v1.0/stations\n
    /api/v1.0/tobs\n
    /api/v1.0/temp/start/end
    ''')

########## /api/v1.0/precipitation #######

@app.route('/api/v1.0/precipitation')
def Precipitation():
    # Create a session
    session = Session(engine)
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    precipation_results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_year).all()
    session.close()
     # Convert list of tuples into normal list
    results = list(np.ravel(precipation_results))
    precip = {date: prcp for date, prcp in precipation_results}
    return jsonify(precip)


######## /api/v1.0/stations route #######

@app.route('/api/v1.0/stations')
def Stations():
    session= Session(engine)
    Stations_results = session.query(Station.station).all()
    results = list(np.ravel(Stations_results) )
    session.close()
    # stations = {station : id  for station,id in Stations_results}
    return jsonify(stations=results)


@app.route('/api/v1.0/tobs')
def Tobs():
    session = Session(engine)
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days= 365)
    tobs_results = session.query(Measurement.date,Measurement.tobs).\
    filter(Measurement.station == 'USC00519281').\
    filter(Measurement.date >= prev_year).all()
    session.close()
    results = list(np.ravel(tobs_results) )

    return jsonify(temps=results)

@app.route('/api/v1.0/temp/start/end')
def Start_End_date():
    session = Session(engine)
    start = input(f"Enter the start date: YYYY-mm-dd : ")
    end = input(f"Enter the enddate: YYYY-mm-dd : ")
     # Query to return the results between the start and end date.
    start_end_results = session.query(\
            Measurement.date,\
            Measurement.station,\
            sqlalchemy.func.max(Measurement.tobs),\
            sqlalchemy.func.min(Measurement.tobs),\
            sqlalchemy.func.avg(Measurement.tobs)\
                ).where((Measurement.date >= start) \
                & (Measurement.date <= end)).all()
    session.close()
    results = list(np.ravel(start_end_results) )

    return jsonify(Aggregate =results)


if __name__ == '__main__':
    app.run(debug=True)

