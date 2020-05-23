from flask import Flask, request, render_template
import os
import csv, base64, time
from random import randint
import random
import pymysql
import pickle
from datetime import datetime
from json import loads, dumps
import requests



application = Flask(__name__)

db = pymysql.connect(user='admin',
                     password='Tharoon123',
                     host='tthiagadbmysql.cmb2u7yd6iyb.us-east-2.rds.amazonaws.com',
                     database = 'tthiagaDB',
                     cursorclass=pymysql.cursors.DictCursor)
# Enter user, password and host. Deleted for security purposes
cursor = db.cursor()

@application.route('/')
def my_form():
    return render_template('index.html')

@application.route('/Display')
def Display():
    return render_template('Display.html')

@application.route('/SET')
def SET  ():
    return render_template('Set.html')



@application.route('/enroll', methods=["POST", "GET"])
def enroll():
    return render_template('enroll.html')

@application.route('/viewClass', methods=["POST", "GET"])
def viewClass():
    query1 = "Select * from Courses"
    start_time = time.time()
    cursor.execute(query1)
    rows = cursor.fetchall()
    end_time = time.time()
    elapsed_time = end_time - start_time
    # r =requests.get('http://tthiaga-env.eba-tcvdfb27.us-east-2.elasticbeanstalk.com/classEnrolled')
    # status = r.status_code
    # head = r.headers['Content-Type']
    # pload = {'utaID':'10012'}
    # re=requests.post('http://tthiaga-env.eba-tcvdfb27.us-east-2.elasticbeanstalk.com/classEnrolled',data = {'utaID':'10012'})
    # result = re.text
    return render_template('viewClass.html', table=rows, elapsed_time = elapsed_time)


@application.route('/classEnrolled', methods=["POST", "GET"])
def classEnrolled():
    utaID = int(request.form.get('utaid'))
    query1 = "Select * from MyCourse where IdNum = '"+str(utaID)+"'"
    cursor.execute(query1)
    rows = cursor.fetchall()
    return render_template('classEnrolled.html', table=rows)


@application.route('/register', methods=["POST", "GET"])
def register():
    utaID = int(request.form.get('utaid'))
    firstName = request.form.get('fname')
    lastName = request.form.get('lname')
    age = int(request.form.get('age'))
    val = (utaID, firstName, lastName, age)

    cid = request.form.get('cid')
    section = request.form.get('section')

    query1 = "Select * from Students where IdNum = '"+str(utaID)+"'"
    cursor.execute(query1)
    result1 = cursor.fetchone()

    if result1 is None:
        query2 = "Insert into Students (IdNum, Fname, Lname, Age, Credit, NoOfClass) VALUES (%s,%s,%s,%s,20,0)"
        cursor.execute(query2, val)
        commit1 = "COMMIT"
        cursor.execute(commit1)
        query3 = "Select * from Students where IdNum = '"+str(utaID)+"'"
        cursor.execute(query3)
        result3 = cursor.fetchall()

    query4 = "Select Credit from Students where IdNum = '"+str(utaID)+"'"
    cursor.execute(query4)
    credit = cursor.fetchone()
    creditResult = credit.get('Credit')

    query5 = "Select Maxseats from Courses where course = '" + str(cid) + "' and section='" + str(section) + "' AND Maxseats!=0"
    cursor.execute(query5)
    maxseats = cursor.fetchone()
    maxseatsResult = maxseats.get('Maxseats')




    query6 = "Select NoOfClass from Students where IdNum = '"+str(utaID)+"'"
    cursor.execute(query6)
    noOfClass = cursor.fetchone()
    noOfClassResult = noOfClass.get('NoOfClass')

    if maxseats is not None and age >= 60 and noOfClassResult < 10 and creditResult >= 10:
        query7 = "Update Courses set Maxseats=Maxseats-1 where Course = '" + str(cid) + "' AND section='" + str(section) + "'"
        cursor.execute(query7)
        commit2 = "COMMIT"
        cursor.execute(commit2)
        query8  = "UPDATE Students SET NoOfClass = NoOfClass+1,Credit=Credit-10 WHERE IdNum = '" + str(utaID) + "'"
        cursor.execute(query8)
        commit3 = "COMMIT"
        cursor.execute(commit3)
        query11 = "INSERT INTO MyCourse VALUES ('" + str(utaID) + "', '" + str(cid) + "', '" + str(section) + "')"
        cursor.execute(query11)
        commit6 = "COMMIT"
        cursor.execute(commit6)
    elif maxseats is not None and age < 60 and noOfClassResult < 10 and creditResult >= 20:
        query9 = "Update Courses set Maxseats=Maxseats-1 where Course = '" + str(cid) + "' AND section='" + str(section) + "'"
        cursor.execute(query9)
        commit4 = "COMMIT"
        cursor.execute(commit4)
        query10  = "UPDATE Students SET NoOfClass = NoOfClass+1,Credit = Credit-20 WHERE IdNum = '" + str(utaID) + "'"
        cursor.execute(query10)
        commit5 = "COMMIT"
        cursor.execute(commit5)
        query12 = "INSERT INTO MyCourse VALUES ('" + str(utaID) + "', '" + str(cid) + "', '" + str(section) + "')"
        cursor.execute(query12)
        commit7 = "COMMIT"
        cursor.execute(commit7)
    else:
        print("")

    query13 = "Select * from Students where IdNum = '"+str(utaID)+"'"
    cursor.execute(query13)
    result13 = cursor.fetchall()


    return render_template('classEnroll.html', table = result13)
    # return render_template('classEnroll.html', credit=credit, maxseats=maxseats, noOfClass = noOfClass, creditResult=creditResult, maxseatsResult=maxseatsResult, noOfClassResult=noOfClassResult)


#############################################################################

@application.route("/volcanocheck", methods=["POST", "GET"])
def volcanocheck():
    vno = int(request.form['vno'])

    sql1 = "SELECT * FROM Volcano WHERE Number= '" + str(vno) + "'"
    cursor.execute(sql1)
    rows = cursor.fetchall()

    return render_template('volcanocheck.html', rows=rows)

@application.route("/volcanoNameUpdate", methods=["POST", "GET"])
def volcanoNameUpdate():
    vno = int(request.form['vno'])
    vname = request.form['vname']

    sql1 = "update Volcano set VolcanoName='" + str(vname) + "' WHERE Number= '" + str(vno) + "'"
    cursor.execute(sql1)
    commit7 = "COMMIT"
    cursor.execute(commit7)

    sql12 = "SELECT * FROM Volcano WHERE Number= '" + str(vno) + "'"
    cursor.execute(sql12)
    rows = cursor.fetchall()
    return render_template('volcanoUpdate.html', rows=rows)


@application.route('/box', methods=['POST', "GET"])
def box():
    latitude1 = request.form['latitude1']
    longitude1 = request.form['longitude1']
    latitude2 = request.form['latitude2']
    longitude2 = request.form['longitude2']
    query1 = "SELECT * from Volcano where Latitude BETWEEN '"+ latitude1 + "' AND  '"+ latitude2 + "' AND Longitude BETWEEN '"+ longitude1 +"' AND '"+ longitude2 + "'"
    cursor.execute(query1)
    rows = cursor.fetchall()
    return render_template('box.html',rows=rows)



@application.route("/elevrange", methods=["POST", "GET"])
def elevrange():
    elevStart = float(request.form['elevStart'])
    elevEnd = float(request.form['elevEnd'])
    net  = float(request.form['increment'])
    start = elevStart
    counts = []
    starts = []
    ends = []
    end = start + net
    while end <= elevEnd:
        query1 = "SELECT * from volcano where Elev >= '"+ str(start) +"' AND Elev <= '" + str(end)+"'"
        cursor.execute(query1)
        result = cursor.fetchall()
        rows = []
        count = 0
        starts.append(start)
        ends.append(end)
        counts.append(len(result))
        start = end
        end = start + net
    length = len(starts)
    return render_template('elevrange.html', starts=starts,ends=ends,counts=counts,length=length)




if __name__ == "__main__":
    application.debug = True
    application.run()
