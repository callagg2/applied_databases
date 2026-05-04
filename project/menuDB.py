# this is the database part of the app based on attendance at a conference, it performs all SQL and neo4j queries

# author: gerry callaghan
# # student number G00472971

import pymysql.cursors
from requests import session
from neo4j import GraphDatabase
from neo4j import exceptions


conn = None

#conn = pymysql.connect("localhost","root","root","school",cursorclass=pymysql.cursors.DictCursor)

# connects to the database
def connect_mysql():
    global conn
    conn = pymysql.connect(host="localhost",user="root",password="root",db="appdbproj",port=3306,cursorclass=pymysql.cursors.DictCursor)

# connects to the neo4j server
def connect_neo4j():
    global driver
    uri = "neo4j://localhost:7687"
    driver = GraphDatabase.driver(uri, auth=("neo4j", "neo4j"), max_connection_lifetime=1000)

# takes in a variable attendee Name or part thereof, and inputs that into a MySQL query before returning various bits of information based on that input
def find_speaker(namestr):
    if (not conn):
        connect_mysql()
    
    query1 = """SELECT session.speakerName, session.sessionTitle, room.roomName FROM session session 
                    inner join room room 
                        on session.roomID = room.roomID 
                where locate(%s, speakerName) != 0 Order by speakerName
            """
    values = ({namestr})
    
    try:
        cursor = conn.cursor()
        cursor.execute(query1,values)
        speakers = cursor.fetchall()
        
    except pymysql.err.InternalError as e:
        print("Speaker: {namestr} doesn't exist",e)
        
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
        
    cursor.close()  # closes the cursor
    return speakers

# takes in a variable company ID, and inputs that into a MySQL query before returning various bits of information based on that input
def find_company(company_id):
    if (not conn):
        connect_mysql()
    
    query4 = "SELECT companyName FROM company where companyID = %s"
    values = company_id
    
    with conn:
        cursor = conn.cursor()
        cursor.execute(query4,values)
        valid_company = cursor.fetchone()
        return valid_company

# takes in a variable company ID, and inputs that into a MySQL query before returning various bits of information based on that input
def view_attendees(company_id):
    if (not conn):
        connect_mysql()
        
        ## using nested joins to get the attendees of a company and the sessions they are registered for, 
        # along with the room and company name, source https://www.navicat.com/en/company/aboutus/blog/1948-nested-joins-explained
        query2 ="""SELECT a.attendeeName, a.attendeeDOB, s.sessionTitle, s.speakerName, s.sessionDate, r.roomName, c.companyName from company c
                INNER JOIN(attendee a INNER JOIN (registration reg 
                INNER JOIN (room r
                INNER JOIN session s 
                on r.roomID = s.roomID) 
                on s.sessionID = reg.sessionID) 
                on a.attendeeID = reg.attendeeID) 
                on a.attendeeCompanyID = c.companyID 
                where companyID = %s order by attendeeName"""  
        values = company_id
        #print(query2)
    

        try:
            cursor = conn.cursor()
            cursor.execute(query2, values)
            company_attendees = cursor.fetchall()
            
            
            #for attendee in attendees:
            #print(attendee["attendeeID"], attendee["attendeeName"], attendee["attendeeDOB"], attendee["attendeeGender"], attendee["attendeeCompanyID"])    
        except pymysql.err. InternalError as e:
            print("Company ID: {company_id} doesn't exist")
    
        cursor.close()  # closes the cursor
        return company_attendees

# takes in a number of inputs and then using MySQL inner joins extracts some information from the different tables
def add_new_attendee(attendee_id, attendee_name, attendee_DOB, attendee_gender, attendee_company_ID):


    if (not conn):
        connect_mysql()
    query3 = "INSERT into attendee (attendeeID, attendeeName, attendeeDOB, attendeeGender, attendeeCompanyID) VALUES (%s, %s, %s, %s, %s)"
    #query3 = "INSERT into attendee (attendeeID, attendeeName, attendeeDOB, attendeeGender, attendeeCompanyID) VALUES (attendee_id, {attendee_name}, {attendee_DOB}, {attendee_gender}, attendee_company_ID)"
    values = (({attendee_id}), ({attendee_name}), ({attendee_DOB}), ({attendee_gender}), ({attendee_company_ID}))
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
            print("\n*** ERROR *** Attendee ID: {attendee_id} already exists, Please try again.")
        except Exception as e:
            print("error",e)
    
    #cursor.close()  # closes the cursor
    #conn.close() # closes the connection

# this functions takes in the attendee IDs and using MYSQL to look up the names of those attendees
def get_names_of_attendees(ids):
	if (not conn):
		connect_mysql()
	
	format_strings = ','.join(['%s'] * len(ids))

	query5 ="Select attendeeID, attendeeName from attendee where attendeeID IN (%s) Order by attendeeID" % format_strings
	
	try:
		cursor = conn.cursor()
		cursor.execute(query5, ids)
		names_of_attendees = cursor.fetchall()
		
	except pymysql.err.InternalError as e:
		print("Attendee ID: {attendees_id} do/does not exist")

	cursor.close()  # closes the cursor
	return names_of_attendees

# this functions is part of the function below, takes in the attendee IDs and uses Neo4j to look up if those attendees are connected
def view_connected_attendees(attendee_id):
    connect_neo4j()
    with driver.session(database="appdbprojNeo4j") as session:
        try:
            results = session.execute_read(return_connected_attendees,attendee_id) # https://neo4j.com/docs/api/python-driver/current/api.html#neo4j.Session.execute_read
            print(results)
            connected_attendees = []
            for result in results:
                connected_attendees.append(result["b.AttendeeID"])        
                return connected_attendees
        except exceptions.ConstraintError as e:
            print("ERROR: ", e.message)

# this function takes in an attendee ID and returns any matches to the ID
def return_connected_attendees(tx,attendee_id):
    query = "MATCH (a:Attendee{AttendeeID:$attendee_id})<-[]->(b:Attendee) RETURN b.AttendeeID"
    results = tx.run(query, attendee_id)
    return results

# this function looks to see if an attendee already exists in the table    
def attendee_preexist_check(attendee_id):
    if (not conn):
        connect_mysql()
    
    query6 = "SELECT attendeeID FROM attendee where attendeeID = %s"
    values = attendee_id
    
    with conn:
        try:
            cursor = conn.cursor()
            cursor.execute(query6, values)
            preexist_attendee = cursor.fetchone()
            return preexist_attendee
        except pymysql.err. InternalError as e:
            print("Attendee ID: {attendee_id} doesn't exist")

# this functions takes in two attendee IDs and add a neo4j connection beteen them, it's part of the function below it
def add_connection(tx, attendee_id_1, attendee_id_2):
    if (not conn):
        connect_neo4j()

    with driver.session(database="appdbprojNeo4j") as session:
        try:
            connection = session.execute_write(add_new_connection, attendee_id_1, attendee_id_2) # https://neo4j.com/docs/api/python-driver/current/api.html#neo4j.Session.execute_write
            print(f"Attendees {attendee_id_1} is now connected to {attendee_id_2}")
        except exceptions.ClientError as e:
            print("***ERROR*** Attendees {attendee_id_1} and {attendee_id_2} are already connected", e)

# this is part of the function above, this is the neo4j query
def add_new_connection(tx, attendee_id_1, attendee_id_2):
    query = "MATCH (a:Attendee {AttendeeID: $attendee_id_1}), (b:Attendee {AttendeeID: $attendee_id_2}) CREATE (a)-[:CONNECTED_TO]->(b)"  
    tx.run(query, attendee_id_1=attendee_id_1, attendee_id_2=attendee_id_2)
    return True

# this function uses MySQL to look up the room information           
def view_rooms():
    if (not conn):
        connect_mysql()
    query5 = "SELECT roomID, roomName, capacity FROM room"
    

    try:
        cursor = conn.cursor()
        cursor.execute(query5)
        rooms = cursor.fetchall()
        return rooms
    except pymysql.err. InternalError as e:
            print("Internal Error")
    
    cursor.close()  # closes the cursor
  