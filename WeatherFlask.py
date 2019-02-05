from flask import Flask,jsonify,request
import numpy as np
from sqlalchemy import and_ ,or_

#Perception Analysis




app=Flask(__name__)
@app.route("/")
def home():
    return(

        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs</br>"
        f"/api/v1.0/?stdate=<br>"
        f"/api/v1.0/?stdate=&enddate=<br>"


    )
@app.route("/api/v1.0/<real_name>")
def RoutersAna(real_name):
    from Routerstest import session,Measurement,Station,func,minyear,minmon,minday,datemon,dateyear


        # Perform a query to retrieve the data and precipitation scores
    if real_name == "precipitation":
        results = session.query(Measurement.date,Measurement.prcp).filter(
            func.extract("year", Measurement.date) >= minyear). \
            filter(or_(
            and_(func.extract("month", Measurement.date) == minmon, func.extract("year", Measurement.date) == minyear,
                 func.extract("day", Measurement.date) >= minday),
            and_(func.extract("month", Measurement.date) > minmon, func.extract("year", Measurement.date) == minyear),
            and_(func.extract("month", Measurement.date) <= datemon,
                 func.extract("year", Measurement.date) == dateyear))).all()

        allprec=[]
        for per in results:
            per_dict={}
            per_dict[per.date]=per.prcp
            allprec.append(per_dict)


        session.close()

        return jsonify(allprec)


    elif real_name=="stations":



        stations = session.query(Station.station).all()
        liststat = list(np.ravel(stations))
        session.close()
        return jsonify(liststat)
    elif real_name=="tobs":


        temptopobse = session.query(Measurement.date,Measurement.tobs).filter(
            func.extract("year", Measurement.date) >= minyear). \
            filter(or_(
            and_(func.extract("month", Measurement.date) == minmon, func.extract("year", Measurement.date) == minyear,
                 func.extract("day", Measurement.date) >= minday),
            and_(func.extract("month", Measurement.date) > minmon, func.extract("year", Measurement.date) == minyear),
            and_(func.extract("month", Measurement.date) <= datemon,
                 func.extract("year", Measurement.date) == dateyear))).all()
        temptopobse1=[res.tobs for res in temptopobse ]

        session.close()
        return jsonify(temptopobse1)
    else:
        return "Please enter the correct URL"


@app.route("/api/v1.0/")
def tobsdates():
    from Routerstest import session, Measurement, Station, func
    strdate = request.args.get("stdate")
    if request.args.get("enddate"):

        enddate = request.args.get("enddate")
        strtemp = session.query(Measurement.date,func.min(Measurement.tobs).label("MinTemp"),
                                func.max(Measurement.tobs).label("MaxTemp"),
                                func.avg(Measurement.tobs).label("AVGTemp")).filter(Measurement.date >= strdate ,Measurement.date<=enddate).group_by(Measurement.date).all()

        session.close()

    else:

        strtemp=session.query(Measurement.date,func.min(Measurement.tobs).label("MinTemp"),func.max(Measurement.tobs).label("MaxTemp"),func.avg(Measurement.tobs).label("AVGTemp") ).filter(Measurement.date>=strdate).group_by(Measurement.date).all()
        session.close()
    mintemplist = [[res.date,res.MinTemp] for res in strtemp]
    maxtemplist = [[res.date,res.MaxTemp] for res in strtemp]
    avgtemplist = [[res.date,res.AVGTemp] for res in strtemp]

    return jsonify(mintemp=mintemplist, maxtem=maxtemplist,avgtem=avgtemplist)


if __name__ == "__main__":
    app.run(debug=True)