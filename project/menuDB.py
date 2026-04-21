import pymysql
from requests import session

conn = None

#conn = pymysql.connect("localhost","root","root","school",cursorclass=pymysql.cursors.DictCursor)

def connect():
    global conn
    conn = pymysql.connect(host="localhost",user="root",password="root",db="appdbproj",port=3306,cursorclass=pymysql.cursors.DictCursor)


def find_speaker(namestr):
    if (not conn):
        connect()
    
    query1 = "SELECT speakerName, sessionTitle, roomID FROM session where locate(%s, speakerName) != 0 Order by speakerName"
    values = ({namestr})
    
    with conn:
        cursor = conn.cursor()
        cursor.execute(query1,values)
        speakers = cursor.fetchall()
        return speakers       
        cursor.close()  # closes the cursor
        #conn.close() # closes the connection
        


def view_attendees(company_id):
    if (not conn):
        connect()
    
    query2 = "SELECT companyID from company WHERE companyID = %s;"
    values = company_id
    #print(query2)
    
    with conn:
        try:
            cursor = conn.cursor()
            cursor.execute(query2, values)
            valid_company = cursor.fetchone()
            return valid_company
            #for attendee in attendees:
                #print(attendee["attendeeID"], attendee["attendeeName"], attendee["attendeeDOB"], attendee["attendeeGender"], attendee["attendeeCompanyID"])    
        except pymysql.err. InternalError as e:
            print("Company ID: {company_id} doesn't exist")
    
    #cursor.close()  # closes the cursor
    #conn.close() # closes the connection











def populate_data(attendee_id, attendee_name, attendee_DOB, attendee_gender, attendee_company_ID):
    if (not conn):
        connect();
    query3 = "INSERT into attendee (attendeeID, attendeeName, attendeeDOB, attendeeGender, attendeeCompanyID) VALUES (%s, %s, %s, %s, %s)"
    #query3 = "INSERT into attendee (attendeeID, attendeeName, attendeeDOB, attendeeGender, attendeeCompanyID) VALUES (attendee_id, {attendee_name}, {attendee_DOB}, {attendee_gender}, attendee_company_ID)"
    values = (({attendee_id}), ({attendee_name}), ({attendee_DOB}), ({attendee_DOB}), ({attendee_company_ID}))
    #print(query)
    
    with conn:
        try:
            cursor = conn.cursor()
            cursor.execute(query3, (values))
            #cursor.execute(query3, (121,"Joe Kelly","1970-02-18","Male",2))
            conn.commit()
            print("Insert Successful")
        except pymysql.err. InternalError as e:
            print("Internal Error")
        except pymysql.err.IntegrityError:
            print("Attendee ID: {attendee_id} already exists")
        except Exception as e:
            print("error",e)
    
    #cursor.close()  # closes the cursor
    #conn.close() # closes the connection
    
        

        
       
 
    
