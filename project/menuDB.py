import mysql
import pymysql
from requests import session
from neo4j import GraphDatabase
from neo4j import exceptions


conn = None

#conn = pymysql.connect("localhost","root","root","school",cursorclass=pymysql.cursors.DictCursor)

def connect_mysql():
    global conn
    connpy = mysql.connections.Connection(host="localhost", user="root", password="root", db="appdbproj", port=3306, cursorclass=pymysql.cursors.DictCursor)

def connect_neo4j():
    global driver
    uri = "neo4j://localhost:7687"
    driver = GraphDatabase.driver(uri, auth=("neo4j", "neo4j"), max_connection_lifetime=1000)

def find_speaker(namestr):
    if (not conn):
        connect_mysql()
    
    query1 = "SELECT speakerName, sessionTitle, roomID FROM session where locate(%s, speakerName) != 0 Order by speakerName"
    values = ({namestr})
    
    with conn:
        try:
            cursor = conn.cursor()
            cursor.execute(query1,values)
            speakers = cursor.fetchall()
            return speakers
        except pymysql.err. InternalError as e:
            print("Speaker: {namestr} doesn't exist")       
    cursor.close()  # closes the cursor
    conn.close() # closes the connection
        
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


def view_attendees(company_id):
    if (not conn):
        connect_mysql()
    
    # using nested joins to get the attendees of a company and the sessions they are registered for, along with the room and company name, source https://www.navicat.com/en/company/aboutus/blog/1948-nested-joins-explained
    query2 =""""SELECT a.attendeeName, a.attendeeDOB, s.sessionTitle, s.speakerName, s.sessionDate, r.roomName, c.companyName 
                from company c 
                    INNER JOIN(attendee a 
                        INNER JOIN (registration reg 
                            INNER JOIN (room r 
                                INNER JOIN session s 
                                    on r.roomID = s.roomID) 
                                on s.sessionID = reg.sessionID) 
                            on a.attendeeID = reg.attendeeID) 
                        on a.attendeeCompanyID = c.companyID 
                where companyID = %s order by attendeeName;"""
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

def get_associated_attendees(tx, attendee_id):
    connect_neo4j()
    with driver.session(database="appdbprojNeo4j") as session:
        values = session.execute_read(get_associated_attendees, attendee_id) # https://neo4j.com/docs/api/python-driver/current/api.html#neo4j.Session.execute_read

    query = "MATCH (a:Attendee{AttendeeID:$attendee_id})<-[]->(b:Attendee) RETURN b.AttendeeID"
    results = tx.run(query, attendee_id=attendee_id)
    connected_attendees = []
    for result in results:
        connected_attendees.append(result["b.AttendeeID"])        
    return connected_attendees

def get_names_of_attendees(attendees_ids):
    if (not conn):
        connect_mysql()
    
    query5 =" select attendeeID, attendeeName from attendee where attendeeID IN $attendees_ids;"
    values = attendees_ids
    #print(query5)
    
    with conn:
        try:
            cursor = conn.cursor()
            cursor.execute(query5, values)
            names_of_attendees = cursor.fetchall()
            return names_of_attendees
                
        except pymysql.err.InternalError as e:
            print("Company ID: {company_id} doesn't exist")

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

           

def add_connection(tx, attendee_id_1, attendee_id_2):
    if (not conn):
        connect_neo4j()

    with driver.session(database="appdbprojNeo4j") as session:
        try:
            connection = session.execute_write(add_new_connection, attendee_id_1, attendee_id_2) # https://neo4j.com/docs/api/python-driver/current/api.html#neo4j.Session.execute_write
            print(f"Attendees {attendee_id_1} is not connected to {attendee_id_2}")
        except exceptions.ClientError as e:
            print("***ERROR*** Attendees {attendee_id_1} and {attendee_id_2} are already connected", e)

def add_new_connection(tx, attendee_id_1, attendee_id_2):
    query = "MATCH (a:Attendee {AttendeeID: $attendee_id_1}), (b:Attendee {AttendeeID: $attendee_id_2}) CREATE (a)-[:CONNECTED_TO]->(b)"  
    tx.run(query, attendee_id_1=attendee_id_1, attendee_id_2=attendee_id_2)


def populate_data(attendee_id, attendee_name, attendee_DOB, attendee_gender, attendee_company_ID):
    if (not conn):
        connect_mysql();
    query3 = "INSERT into attendee (attendeeID, attendeeName, attendeeDOB, attendeeGender, attendeeCompanyID) VALUES (%s, %s, %s, %s, %s)"
    #query3 = """INSERT into attendee (attendeeID, attendeeName, attendeeDOB, attendeeGender, attendeeCompanyID) 
                # VALUES (attendee_id, {attendee_name}, {attendee_DOB}, {attendee_gender}, attendee_company_ID)"""
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
            print("Attendee ID: {attendee_id} already exists")
        except Exception as e:
            print("error",e)
    
    #cursor.close()  # closes the cursor
    #conn.close() # closes the connection

def view_rooms():
    if (not conn):
        connect_mysql()
    query5 = "SELECT roomID, roomName, capacity FROM room"
    
    with conn:
        try:
            cursor = conn.cursor()
            cursor.execute(query5)
            rooms = cursor.fetchall()
            return rooms
        except pymysql.err. InternalError as e:
            print("Internal Error")
    



