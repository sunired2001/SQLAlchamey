from sqlalchemy import and_ ,or_
import datetime
from datetime import timedelta

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)
session = Session(engine)
Measurement = Base.classes.measurement
Station = Base.classes.station
query1 = session.query(func.max(func.extract("year", Measurement.date)))
query2 = session.query(func.max(func.extract("month", Measurement.date))).filter(
func.extract("year", Measurement.date) == query1)
query3 = session.query(func.max(func.extract("day", Measurement.date))). \
filter(func.extract("year", Measurement.date) == query1, func.extract("month", Measurement.date) == query2)
for res in query1:
    dateyear = int(res[0])
for res in query2:
    datemon = int(res[0])
for res in query3:
    dateday = int(res[0])
            # .strftime("%Y-%m-%d")
minyear = (datetime.datetime(dateyear, datemon, dateday) - timedelta(days=365)).strftime("%Y")
minmon = (datetime.datetime(dateyear, datemon, dateday) - timedelta(days=365)).strftime("%m")
minday = (datetime.datetime(dateyear, datemon, dateday) - timedelta(days=365)).strftime("%d")