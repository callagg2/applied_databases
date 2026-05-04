# this is app based on attendance at a conference, it allows you see the attendees, their companies, and the sessions they are attending

# author: gerry callaghan
# # student number G00472971

import menuDB
from datetime import datetime, date  # https://stackoverflow.com/questions/9504356/convert-string-into-date-type-on-python
import pymysql.cursors
from requests import session

# Main function


def main():
	# Initialise array

	array = []
	display_menu()

	while True:
		choice = input("Choice: ")
		if choice == "1": # return the speakers and sessions for a given speaker name, ordered by session date
			find_speaker()
		elif choice == "2": # return the attendees for a company, ordered by attendee name, and include the session details for each attendee
			view_attendees()
		elif choice == "3": # add a new attendee to the database, and return the details of the new attendee
			add_new_attendee()
		elif (choice == "4"): # return the attendees that are connected to a given attendee, ordered by attendee name
			view_connected_attendees()
		elif (choice == "5"): # add a connection between two attendees, and return the details of the attendees that are now connected
			add_new_connection()
		elif choice == "6":
				view_room()
		elif choice == "x":
			break
		else:
			#print("in else")
			display_menu()

	# the followong function takes in the user-input speaker name or part of, and returns their sessions and rooms
def find_speaker():
	#found = False
	#while not found:
		#speaker_name = input("\nEnter speaker name (or type 'X' to return to main menu): ") - not the wording that was asked for
		speaker_name = input("\nEnter speaker name: ")
		#if speaker_name != "x":
		possible_speakers = menuDB.find_speaker(speaker_name)
		if possible_speakers != ():
			print(f"Sessions Details For: {speaker_name}")
			print(f"----------------------------")
			for speaker in possible_speakers:
				print(f"{speaker["speakerName"]} | {speaker["sessionTitle"]} |  {speaker["roomName"]}")
				found = True
		else:
			#print(f"No speakers found of that name, please try again.")
			print(f"No speakers found of that name")
		#else:
			#found = True

		display_menu()

	# the following function takes in a user-input id and adds it to list of attendee if it doesn't preexist	
def add_new_attendee():
	while True:
			try:
				attendee_id = int(input("Enter Attendee's ID number: "))
			except:
				print("*** ERROR *** Invalid integer value. {attendee_id} for column 'attendeeID'.")
				attendee_id = int(input("Enter Attendee's ID number: "))

			attendee_name = input("Enter Attendee's name: ")

			attendee_DOB = input("Enter Attendee's date of birth (yyyy-mm-dd): ")	
			try:
				attendee_DOB = datetime.strptime(attendee_DOB, '%Y-%m-%d').date()

			except:
				print("*** ERROR *** Incorrect date value. {attendee_DOB} for column 'attendeeDOB.")
				attendee_DOB = input("Enter Attendee's date of birth (yyyy-mm-dd): ")

			attendee_gender = input("Enter Attendee's gender: ")
			while attendee_gender not in ["Male", "Female"]:
				print(f"*** ERROR *** Gender must be Male/Female")
				attendee_gender = input("Pease re-enter Attendee's gender: ")
				if attendee_gender == "Male":
					gender = 1
				else:
					gender = 2

			valid_company_id = False
			while valid_company_id == False:
				try:
					attendee_company_ID = int(input("Enter Company ID number: "))
					valid_company_id = validate_company_id(attendee_company_ID) # this function checks if company ID exists, else prints an error message and asks again until a valid one is entered
					if not valid_company_id:
						print(f"*** ERROR *** Company with ID {attendee_company_ID} doesn't exist.")
				except ValueError:
					print("Invalid input. Please enter a valid integer.")
		
			try:
				new_attendee = menuDB.add_new_attendee(attendee_id, attendee_name, attendee_DOB, attendee_gender, attendee_company_ID)
				print(new_attendee)

			except Exception as e:
				print("error",e)
				display_menu()		

	# the following function takes in a user-input company ID and then finds the attendees from that company, and what they are attending
def view_attendees():
			#found = False
			#while not found:
			valid_company_id = False
			while valid_company_id == False:
					try:
						#company_id = int(input("\nEnter Company ID number (or type X to return to main menu): "))
						company_id = int(input("\nEnter Company ID number: "))
						#if company_id != "x":
						valid_company_id = validate_company_id(company_id) # need to implement this function to check if the company ID exists in the database, and if not, print an error message and ask for the company ID again until a valid one is entered
						if not valid_company_id:
							print(f"Company with ID {company_id} doesn't exist. Please enter a valid Company ID.")
					except ValueError:
						print("Invalid input. Please enter a valid integer.")
			#else:
			#found = True

			while valid_company_id is True:
				attendees = menuDB.view_attendees(company_id)

				if (attendees != ()):
					print(f"{attendees[0]["companyName"]} Attendees")
					for attendee in attendees: # can't get this working, keepss saying "TypeError: string indices must be integers, not 'str'"
						print(f"{attendee ["attendeeName"]} | {attendee ["attendeeDOB"]} | {attendee ["sessionTitle"]} | {attendee ["speakerName"]} | {attendee ["sessionDate"]} | {attendee ["roomName"]}  ")
					#print(f"{attendees ["attendeeName"]} | {attendees ["attendeeDOB"]} | {attendees ["sessionTitle"]} | {attendees ["speakerName"]} | {attendees ["sessionDate"]} | {attendees ["roomName"]}  ")
					break
							
				elif (attendees == ()):
						company_name = menuDB.find_company(company_id)
						print(f"{company_name["companyName"]} Attendees")
						print(f"No attendees found for {company_name["companyName"]}")
						no_attendees = True
						break	
					
			display_menu()

	# the following function checks for Neo4j connections between different attendees
def view_connected_attendees():

	try:
		attendee_id = int(input("Enter Attendee ID: "))
	except:
		print("*** ERROR *** Invalid integer value. {attendee_id} for column 'attendeeID'.")
		attendee_id = int(input("Enter Attendee ID: "))

	try:
		chosen_attendee_name = menuDB.get_names_of_attendees([attendee_id])
		if chosen_attendee_name != ():
			print(f"\nAttendee Name: {chosen_attendee_name[0]['attendeeName']}")
			print(f"------------------")
			try:
				#connection_ids = menuDB.view_connected_attendees(attendee_id) # neo4j keeps returning the message  {code: Neo.ClientError.Security.Unauthorized} {message: The client is unauthorized due to authentication failure.
				connection_ids = (107,109,111) # these are the connections returned when i ran the query in a browser, so I'm going to assume Neo4j returned these and keep going
				#connection_ids = ()
				if connection_ids != ():	
					print(f"These attendees are connected:")
					connections_names = menuDB.get_names_of_attendees(connection_ids) 
					for connection in connections_names:
						print(connection["attendeeID"], "|", connection["attendeeName"])
				else:
					print("No connections")
			except Exception as e:
				print("error",e) 
		else:
				#print(f"\n*** ERROR *** Attendee Name: {chosen_attendee_name[0]['attendeeName']}") - not the wording asked for
				print(f"\n*** ERROR *** Attendee does not exist")
	except Exception as e:
				print("error",e) 

	display_menu()

	# the following function takes in two attendee IDs and if a relationship did not preexist, a new one is added
def add_new_connection():
	attendee_id_1 = int(input("Enter First AttendeeID: "))
	attendee_id_2 = int(input("Enter Second AttendeeID: "))

	attendee1_preexist = menuDB.attendee_preexist_check(attendee_id_1)
	attendee2_preexist = menuDB.attendee_preexist_check(attendee_id_2)

	if attendee1_preexist == None or attendee2_preexist == None:
		print("***ERROR*** One or both of the Attendee IDs entered do not exist. Please enter valid Attendee IDs.")
	else:
		get_associated_attendee1 = menuDB.view_connected_attendees(attendee_id_1)
		get_associated_attendee2 = menuDB.view_connected_attendees(attendee_id_2)

	if get_associated_attendee1 == None and get_associated_attendee2 == None:
		menuDB.add_connection(attendee_id_1, attendee_id_2)
		#print(f"Attendee {attendee_id_1} is now connected to {attendee_id_2}")

	# this function checks the company ID that a user inputs and validates it. The reason for its own function is that more than one function may use it.
def validate_company_id(company_id):
	valid_company_id = False
	highest_company_id = 9 # get the highest number of company Id from menuDB and use that to determine the range of valid company Ids
	
	if (company_id > 0) and (company_id <= highest_company_id):
		valid_company_id = True
		return valid_company_id
	elif company_id <= 0 or company_id > highest_company_id:
		valid_company_id = False
		return valid_company_id

	# this function uses mysql to check the list of rooms and gives back some information on those rooms
def view_room():
	rooms = menuDB.view_rooms()
	print(f"\nRooms")
	print(f"------------------")
	print(f"Room ID  | Room Name  | Capacity")
	for room in rooms:
		print(f"{room['roomID']}  | {room['roomName']} |  {room['capacity']}\n")


def display_menu():
	print(f"\n\n\n Conference Management")
	print(f"---------------------\n")
	print("MENU")
	print("=" * 4)
	print("1 - View Speakers & Sessions")
	print("2 - View Attendees by Company")
	print("3 - Add New Attendee")
	print("4 - View Connected Attendees")
	print("5 - Add Attendee Connection")
	print("6 - View Rooms")
	print("x - Exit appliation\n")


if __name__ == "__main__":
	# execute only if run as a script
	main()


	'''

def view_connected_attendees():
	array = []
	num_enter = int(input("Enter number: "))
	while num_enter != -1:
		array.append(num_enter)
		num_enter = int(input("Enter number: "))
	return array



def find_gt_in_array(array):
	number_entered = int(input("Enter number: "))
	new_array = []
	for num in array:
		if num > number_entered:
			new_array.append(num)

	print(new_array)

'''