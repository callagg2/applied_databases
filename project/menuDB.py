import pymysql

conn = None

#conn = pymysql.connect("localhost","root","root","school",cursorclass=pymysql.cursors.DictCursor)

def connect():
    global conn
    conn = pymysql.connect(user="root",password="root",host="localhost",db="appdbproj",port=3306,cursorclass=pymysql.cursors.DictCursor)

def populate_data(attendee_id, attendee_name, attendee_DOB, attendee_gender, attendee_company_ID):
    if (not conn):
        connect();
    #attendee_id = 121
    #attendee_name = "Joe Kelly"
    attendee_DOB = "1970-02-18"
    attendee_gender = "Male"
    #attendee_company_ID = 2
    #Executing a query
    #query = "INSERT into attendee (attendeeID, attendeeName,  attendeeCompanyID) VALUES (%s, %s, %s)"
    #values = ({attendee_id}, "{attendee_name}", {attendee_company_ID})
    query = "INSERT into attendee (attendeeID, attendeeName, attendeeDOB, attendeeGender, attendeeCompanyID) VALUES (%s, %s, %s, %s, %s)"
    values = ({attendee_id}, "{attendee_name}", "{attendee_DOB}", "{attendee_gender}", {attendee_company_ID})
        
    #query = "SELECT * from attendee"

    with conn:
        cursor = conn.cursor()
        #cursor.execute(query)
        cursor.execute(query, values)
        attendees = cursor.fetchall()
        for attendee in attendees:
            print(attendee["attendeeID"], attendee["attendeeName"], attendee["attendeeCompanyID"])
            #print(attendee["attendeeID"], attendee["attendeeName"], attendee["attendeeDOB"], attendee["attendeeGender"], attendee["attendeeCompanyID"])
        #print (attendees)
    
