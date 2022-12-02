import io
import os
import stat
from codecs import encode
import logging
from flask import Flask, render_template, request, jsonify,session
import pandas as pd
import mysql.connector as conn
import base64





class sqlClass:
    LOG_FILE_NAME = 'BookMyHall.log'
    LOG_FILE_DIR = os.path.join(os.getcwd(), "logs")
    os.makedirs(LOG_FILE_DIR, exist_ok=True)
    LOG_FILE_PATH = os.path.join(LOG_FILE_DIR, LOG_FILE_NAME)
    logging.basicConfig(filename=LOG_FILE_PATH, level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

    def sqlLogin(self, app, host, user, passwd):
        self.app = app
        self.host = host
        self.user = user
        self.passwd = passwd
        try:
            mydb = conn.connect(host=self.host, user=self.user, passwd=self.passwd)
            cursor = mydb.cursor()
            logging.info('Connection Done..')
            return 'Done'
        except Exception as e:
            return "Failed"
            logging.exception("Not Able to connect ", e)



    def homePage(self, dbName, tableNames):
        try:
            self.dbName = dbName
            self.tableNames = tableNames

            mydb = conn.connect(host=self.host, user=self.user, passwd=self.passwd)
            cursor = mydb.cursor()

            cursor.execute("select * from "+self.dbName+"."+self.tableNames[0]+';')
            hallImageQuery = cursor.fetchall()


            cursor.execute("select * from " + self.dbName + "." + self.tableNames[1] + ';')
            homeImageQuery = cursor.fetchall()
            logging.info("Rendering Home Page.")
            return [hallImageQuery,homeImageQuery]
        except Exception as e:
            logging.exception("Table Creation may Occure problem ", e)
            return str(e)

    def credentialSave(self, dbname, tablename, name,email, pwd):
        try:
            self.dbname = dbname
            self.tablename = tablename
            self.name = name
            self.email = email
            self.pwd = pwd

            mydb = conn.connect(host=self.host, user=self.user, passwd=self.passwd)

            cursor = mydb.cursor()
            cursor.execute(
                '(select count(*) from '+self.dbname+'.'+self.tablename+');'
            )
            col = cursor.fetchall()
            rowCount = 0
            for x in col:

                rowCount = int(x[0])
            rowCount = rowCount+1

            cursor.execute(
                'insert into '+self.dbname+'.'+self.tablename+' values('+str(rowCount)+',"'+self.name+'","'+self.email+'","'+self.pwd+'");'
            )

            mydb.commit()
            logging.info("credentialSave()....")
            return [self.name,self.email]
        except Exception as e:
            logging.exception("Table Creation may Occure problem ", e)


    def gettingInfo(self,dbname, tablename, name):
        try:

            self.dbname = dbname
            self.tablename = tablename
            self.name = name
            mydb = conn.connect(host=self.host, user=self.user, passwd=self.passwd)
            cursor = mydb.cursor()
            cursor.execute("select email from " + self.dbname + "." + self.tablename + " where name in ('" +self.name+ "')")
            sql_query = cursor.fetchall()
            for credential in sql_query:
                logging.info("gettingInfo()....")
                return credential
        except Exception as e:
            logging.exception("gettingInfo() may Occure problem ", str(e))

    def credentialCheck(self,dbname, tablename, email, pwd):
        try:

            self.dbname = dbname
            self.tablename = tablename
            self.email = email
            self.pwd = pwd

            mydb = conn.connect(host=self.host, user=self.user, passwd=self.passwd)
            cursor = mydb.cursor()
            cursor.execute("select * from "+self.dbname+"."+self.tablename)
            sql_query = cursor.fetchall()
            for credential in sql_query:
                if self.email == credential[2]:
                    if self.pwd == credential[3]:return [credential[1],credential[2],credential[3],credential[4]]
                    logging.info("User name and password is correct....")
                    return 'PassWord Incorrect'
            return 'UserName or Email Incorrect'

        except Exception as e:
            logging.exception("credentialCheck() may Occure problem ", str(e))


    def fetchVandorDetails(self,  dbName, tableName, hallName):
        try:
            self.dbName = dbName
            self.tableName = tableName
            self.hallName = hallName
            mydb = conn.connect(host=self.host, user=self.user, passwd=self.passwd)
            cursor = mydb.cursor()
            cursor.execute("select * from "+ self.dbName + "." + self.tableName +" where HALL_NAME = '"+self.hallName+"'")
            allDetails = cursor.fetchall()

            for detail in allDetails:
                logging.info("vendor details is successfully fetched....")
                return detail
        except Exception as e:
            logging.exception("fetchVandorDetails() may Occure problem ", str(e))


    def dateConfirmation(self,dbName, tableName, values):
        try:
            self.dbName = dbName
            self.tableName = tableName
            self.values = values
            mydb = conn.connect(host=self.host, user=self.user, passwd=self.passwd)


            cursor = mydb.cursor()

            cursor.execute(
                '(select date from ' + self.dbName + '.' + self.tableName + " where date = '"+ self.values[3]+"'  and hall='"+self.values[5]+"');"
            )
            sql_query = cursor.fetchall()
            if len(sql_query) == 0:
                cursor = mydb.cursor()
                cursor.execute(
                    '(select count(*) from ' + self.dbName + '.' + self.tableName + ');'
                )
                col = cursor.fetchall()
                rowCount = 0
                for x in col:
                    rowCount = int(x[0])
                rowCount = rowCount + 1

                cursor.execute(
                    'insert into ' + self.dbName + '.' + self.tableName + ' values(' + str(rowCount) + ',"' +
                    self.values[
                        0] + '","' + self.values[1] + '","' + self.values[2] + '","' + self.values[3] + '","' +
                    self.values[
                        4] + '","' + self.values[5] +'");'
                )

                # logging.info("Table is created..")
                mydb.commit()
                logging.info("Booking is done....")
                return 'Avail'
            logging.info("Booking is not done because hall is housefull....")
            return "Not Avail"



        except Exception as e:
            logging.exception("dateConfirmation() may Occure problem ", str(e))
            return str(e)


    def queriesOfUser(self, dbName, tableName, values):
        try:
            self.dbName = dbName
            self.tableName = tableName
            self.values = values
            mydb = conn.connect(host=self.host, user=self.user, passwd=self.passwd)
            cursor = mydb.cursor()

            cursor.execute('(select count(*) from ' + self.dbName + '.' + self.tableName + ');')
            col = cursor.fetchall()
            rowCount = 0
            for x in col:

                rowCount = int(x[0])
            rowCount = rowCount + 1

            cursor.execute(
                'insert into ' + self.dbName + '.' + self.tableName + ' values(' + str(rowCount) + ',"' + self.values[0] + '","' + self.values[1] + '","' + self.values[2] + '","' + self.values[3] + '","' + self.values[4] + '");'
                            )

            logging.info("User Queries is successfully inserted..")
            mydb.commit()

            return 'Done'
        except Exception as e:
            logging.exception("queriesOfUser() may Occure problem ", str(e))
            return str(e)


    def modifyDetail(self,dbname, tablename, name, email, pwd):
        try:

            self.name = name
            self.dbname = dbname
            self.tablename = tablename
            self.email = email
            self.pwd = pwd

            mydb = conn.connect(host=self.host, user=self.user, passwd=self.passwd)
            cursor = mydb.cursor()
            cursor.execute('SET SQL_SAFE_UPDATES=0;')
            cursor.execute("UPDATE "+self.dbname+"."+self.tablename+" SET password ='"+self.pwd+"', name='"+self.name+"' WHERE email='"+self.email+"';")
            cursor.execute('SET SQL_SAFE_UPDATES=1;')
            mydb.commit()

            return 'UserName or Password Updated'

        except Exception as e:
            logging.exception("modifyDetail() may Occure problem ", str(e))
            return ''

    def savingBooking(self,dbname, tablename, email, bookingStatus):
        try:
            self.dbname = dbname
            self.tablename = tablename
            self.email = email
            self.bookingStatus = bookingStatus

            mydb = conn.connect(host=self.host, user=self.user, passwd=self.passwd)
            cursor = mydb.cursor()
            cursor.execute('SET SQL_SAFE_UPDATES=0;')
            cursor.execute("UPDATE " + self.dbname + "." + self.tablename + " SET document ='" + self.bookingStatus + "' WHERE email='" + self.email + "';")
            cursor.execute('SET SQL_SAFE_UPDATES=1;')
            mydb.commit()

            return 'UserName or Password Updated'

        except Exception as e:
            logging.exception("savingBooking() may Occure problem ", str(e))
            return 0


hallsImgList = []
homePgImgList = []
hallNameList = []
def fecthData(hallContentImage,homePageContentImage):
    for image in hallContentImage:
        imagecode = image[2]
        imageName = image[1]
        binary_data = base64.b64encode(imagecode)
        binary_data = str(binary_data)
        binary_data = binary_data[2:-1]
        hallsImgList.append(binary_data)
        hallNameList.append(imageName)

    for _ in homePageContentImage:
        imagecode = _[2]
        binary_data = base64.b64encode(imagecode)
        binary_data = str(binary_data)
        binary_data = binary_data[2:-1]
        homePgImgList.append(binary_data)
    return [hallsImgList,hallNameList,homePgImgList]


appObj = Flask(__name__)
appObj.secret_key = 'mohit1234'
app = sqlClass()

app.sqlLogin(appObj,'localhost','root','Survival@0418')

hallContentImage,homePageContentImage = app.homePage('Hall_Details_DB',['vandor_details_table','home_images'])
hallsImgList,hallNames, homePgContentImage = fecthData(hallContentImage,homePageContentImage)

@appObj.route('/', methods=['GET', 'POST']) # To render Homepage
def home_page():
    global checking_flag

    checking_flag = 0
    vlink = '/login.html'
    if ('user' in session) and (session['email'] == 'mohitchatterjee07@gmail.com'): return render_template('home.html', result=([hallsImgList, hallNames, homePgContentImage, session['user']+'(admin)',vlink]))
    elif ('user' in session) : return render_template('home.html', result=([hallsImgList, hallNames, homePgContentImage, session['user'],vlink]))
    else:
        value = 'Sign up/Sign in'
        return render_template('home.html',result=([hallsImgList,hallNames,homePgContentImage,value,vlink]))


#---------------------------------------------Login/Logout Pg-------------------------------------------------


@appObj.route('/login.html', methods=['GET', 'POST'])
def loginPg():
    global flag
    flag =  'login'
    return render_template('login.html')

@appObj.route('/logout',  methods=['GET', 'POST'])
def logout():
    if 'user' in session:
        if 'hall_Name' in session:
            if 'booking_date' in session :
                if 'results'  in session:
                    session.pop('user')
                    session.pop('email')
                    session.pop('psw')
                    session.pop('hall_Name')
                    session.pop('booking_date')
                    session.pop('results')
                    value = 'Sign up/Sign in'
                    return render_template('home.html', result=([hallsImgList, hallNames, homePgContentImage, value]))
                else:
                    session.pop('user')
                    session.pop('email')
                    session.pop('psw')
                    session.pop('hall_Name')
                    session.pop('booking_date')
                    value = 'Sign up/Sign in'
                    return render_template('home.html', result=([hallsImgList, hallNames, homePgContentImage, value]))
            else:
                session.pop('user')
                session.pop('email')
                session.pop('psw')
                session.pop('hall_Name')
                value = 'Sign up/Sign in'
                return render_template('home.html', result=([hallsImgList, hallNames, homePgContentImage, value]))
        else:
            session.pop('user')
            session.pop('email')
            session.pop('psw')
            value = 'Sign up/Sign in'
            return render_template('home.html', result=([hallsImgList, hallNames, homePgContentImage, value]))
    return render_template('login.html')


@appObj.route('/signup.html', methods=['GET', 'POST'])
def signUpPg():
    global flag
    flag = 'sign up'

    if ('user' in session):
        details = app.gettingInfo('Hall_Details_DB', 'credential_table', session['user'])
        if details == None: return render_template('signup.html')
        elif (session['email'] == 'mohitchatterjee07@gmail.com'): return render_template('adminProfilePg.html', result=[session['user'], details[0]])
        return render_template('profilePg.html', result=[session['user'], details[0]])
    return render_template('signup.html')

@appObj.route('/signUpsignIn', methods=['POST'])  # This will be called from UI
def signUpAndLogin():
    global checking_flag
    global info

    if flag == 'login':
        email = request.form['loginUser']
        psw = request.form['loginPassword']
        info = app.credentialCheck('Hall_Details_DB','credential_table',email,psw)

        if info[1] == email:
            session['user'] = info[0]
            session['email'] = info[1]
            session['psw'] = info[2]
            session['bookingCnfrm'] = info[3]
            checking_flag = 1
            if ('user' in session) and (session['email'] == 'mohitchatterjee07@gmail.com'):return render_template('home.html', result=([hallsImgList, hallNames, homePgContentImage, session['user'] + '(admin)']))
            return render_template('home.html',result=([hallsImgList, hallNames, homePgContentImage, session['user']]))
        return render_template('errorPg.html', result=info)

    elif flag == 'sign up':
        name = request.form['name']
        email = request.form['email']
        psw = request.form['psw']
        session['email'] = email
        session['user'] = name
        session['psw'] = psw

        info = app.credentialSave('Hall_Details_DB', 'credential_table', name, email, psw)
        checking_flag = 2

        if ('user' in session) and (session['email'] == 'mohitchatterjee07@gmail.com'): return render_template('home.html',result=([hallsImgList, hallNames, homePgContentImage, session['user'] + '(admin)']))
        return render_template('home.html', result=([hallsImgList, hallNames, homePgContentImage, session['user']]))


@appObj.route('/editDetail', methods=['GET', 'POST'])
def editingDetails():return render_template('editDetails.html',result=[session['email'],session['user'],session['psw']])


@appObj.route('/editingDone', methods=['GET', 'POST'])
def editingDoneDetails():
    name = request.form['name']
    email = request.form['email']
    psw = request.form['psw']
    session['email'] = email
    session['user'] = name
    session['psw'] = psw

    modifyState = app.modifyDetail('Hall_Details_DB', 'credential_table', name, email, psw)
    if session['email'] == 'mohitchatterjee07@gmail.com': return render_template('adminProfilePg.html', result=[session['user'], session['email']])
    return render_template('profilePg.html', result=[session['user'], session['email']])


#---------------------------------------------Login/Logout Pg-------------------------------------------------

@appObj.route('/contact_us.html', methods=['GET', 'POST'])
def contactUs_pg():return render_template('contact_us.html',)

@appObj.route('/profilePg.html', methods=['GET', 'POST'])
def profilePg():

    if (checking_flag > 0 or 'user' in session) and session['email'] == 'mohitchatterjee07@gmail.com': return render_template('adminProfilePg.html', result=[session['user'], session['email']])
    elif (checking_flag > 0 or 'user' in session):return render_template('profilePg.html', result=[session['user'], session['email']])
    else:
        global flag
        flag = 'sign up'
        return render_template('signup.html',result=[['','']])


#----------------------------------------------------------------HALLs---------------------------------------------------------

@appObj.route('/halls/AllHall/JalsaNew', methods=['GET', 'POST'])
def jalsa_pg():
    vandorDetails = app.fetchVandorDetails('Hall_Details_DB', 'vandor_details_table', hallNames[0])

    session['hall_Name'] = hallNames[0]

    featureList = vandorDetails[6].split('@')
    buffetVar = featureList[0]
    receptionVar = featureList[1]
    cafeteriaVar = featureList[2]
    safetyVar = featureList[3]
    additionalServicesVar = featureList[4]

    servicesList = [buffetVar, receptionVar, cafeteriaVar, safetyVar, additionalServicesVar]
    if 'user' in session:
        userEmail = app.gettingInfo('Hall_Details_DB', 'credential_table', session['user'])
        return render_template('/halls/halls.html', result=[hallsImgList,vandorDetails,session['user'],userEmail[0],servicesList])
    else:
        headerPart = 'SignUp/SignIn'
        return render_template('/halls/halls.html', result=[hallsImgList,vandorDetails, headerPart,'',servicesList])

@appObj.route('/halls/AllHall/Lagan_Palace', methods=['GET', 'POST'])
def Lagan_Palace():
    vandorDetails = app.fetchVandorDetails('Hall_Details_DB', 'vandor_details_table', hallNames[1])

    session['hall_Name'] = hallNames[1]

    featureList = vandorDetails[6].split('@')
    buffetVar = featureList[0]
    receptionVar = featureList[1]
    cafeteriaVar = featureList[2]
    safetyVar = featureList[3]
    additionalServicesVar = featureList[4]

    servicesList = [buffetVar, receptionVar, cafeteriaVar, safetyVar, additionalServicesVar]
    if 'user' in session:
        userEmail = app.gettingInfo('Hall_Details_DB', 'credential_table', session['user'])
        return render_template('/halls/halls.html', result=[hallsImgList,vandorDetails,session['user'],userEmail[0],servicesList])
    else:
        headerPart = 'SignUp/SignIn'
        return render_template('/halls/halls.html', result=[hallsImgList,vandorDetails, headerPart,'',servicesList])

@appObj.route('/halls/AllHall/Subham Palace', methods=['GET', 'POST'])
def SubhamPalacepg():
    vandorDetails = app.fetchVandorDetails('Hall_Details_DB', 'vandor_details_table', hallNames[2])

    session['hall_Name'] = hallNames[2]

    featureList = vandorDetails[6].split('@')
    buffetVar = featureList[0]
    receptionVar = featureList[1]
    cafeteriaVar = featureList[2]
    safetyVar = featureList[3]
    additionalServicesVar = featureList[4]

    servicesList = [buffetVar, receptionVar, cafeteriaVar, safetyVar, additionalServicesVar]
    if 'user' in session:
        userEmail = app.gettingInfo('Hall_Details_DB', 'credential_table', session['user'])
        return render_template('/halls/halls.html', result=[hallsImgList,vandorDetails,session['user'],userEmail[0],servicesList])
    else:
        headerPart = 'SignUp/SignIn'
        return render_template('/halls/halls.html', result=[hallsImgList,vandorDetails, headerPart,'',servicesList])

@appObj.route('/halls/AllHall/Surya International', methods=['GET', 'POST'])
def SuryaInternationalpg():
    vandorDetails = app.fetchVandorDetails('Hall_Details_DB', 'vandor_details_table', hallNames[3])

    session['hall_Name'] = hallNames[3]

    featureList = vandorDetails[6].split('@')
    buffetVar = featureList[0]
    receptionVar = featureList[1]
    cafeteriaVar = featureList[2]
    safetyVar = featureList[3]
    additionalServicesVar = featureList[4]

    servicesList = [buffetVar, receptionVar, cafeteriaVar, safetyVar, additionalServicesVar]
    if 'user' in session:
        userEmail = app.gettingInfo('Hall_Details_DB', 'credential_table', session['user'])
        return render_template('/halls/halls.html', result=[hallsImgList,vandorDetails,session['user'],userEmail[0],servicesList])
    else:
        headerPart = 'SignUp/SignIn'
        return render_template('/halls/halls.html', result=[hallsImgList,vandorDetails, headerPart,'',servicesList])


#----------------------------------------------------------------HALLs---------------------------------------------------------


#-----------------------------------------------------------Payment-----------------------------------------------------------


@appObj.route('/paymentAction', methods=['GET', 'POST'])
def payment_pg():

    name = request.form['name']
    email = request.form['email']
    address = request.form['address']
    city = request.form['city']
    state = request.form['state']
    zip = request.form['zip']
    amount = request.form['amount']
    results = [session['user'],email,address,city,state,zip,amount,session['hall_Name'],session['booking_date']]
    session['results'] = results
    app.savingBooking('Hall_Details_DB', 'credential_table',session['email'],'yes')
    return render_template('bookingHallPg.html', result=results)

@appObj.route('/bookingReport', methods=['GET', 'POST'])
def bookingReport_pg():

    info = app.credentialCheck('Hall_Details_DB', 'credential_table', session['email'], session['psw'])
    if info[3] == 'yes': return render_template('bookingHallPg.html', result=session['results'])
    return render_template('/halls/reportNotAvail.html')

#-----------------------------------------------------------Payment-----------------------------------------------------------

@appObj.route('/queries', methods=['GET', 'POST'])  # This will be called from UI
def userQueries():
        if ('user' in session):
            Name = request.form['Name']
            Email = request.form['Email']
            People = request.form['People']
            Date = request.form['date']
            Message = request.form['Message']
            session['booking_date'] = Date
            val = app.dateConfirmation('Hall_Details_DB','queries',[Name,Email,People,Date,Message,session['hall_Name']])
            if val == 'Avail': return render_template('Paymentpg.html',result=[session['hall_Name'],session['user']])
            return render_template('BookingFailPg.html')
        return render_template('signup.html')

if __name__ == '__main__':
    appObj.run()

