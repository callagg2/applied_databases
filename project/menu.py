import menuDB
from datetime import datetime, date  # https://stackoverflow.com/questions/9504356/convert-string-into-date-type-on-python

# Main function


def main():
	# Initialise array
	array = []
	display_menu()

	while True:
		choice = input("Choice: ")

		if choice == "1": # return the speakers and sessions for a given speaker name, ordered by session date
			speaker_name = input("\nEnter speaker name: ")
			
			possible_speakers = menuDB.find_speaker(speaker_name)
			if possible_speakers != ():
				print(f"Sessions Details For: {speaker_name}")
				print(f"----------------------------")
				for speaker in possible_speakers:
					print(f"{speaker["speakerName"]} | {speaker["sessionTitle"]} |  {speaker["roomID"]}")
			else:
				print(f"No speakers found of that name")
			

			display_menu()
			

		elif choice == "2": # return the attendees for a company, ordered by attendee name, and include the session details for each attendee
			valid_company_id = False
			while valid_company_id == False:
					try:
						company_id = int(input("\nEnter Company ID number: "))
						valid_company_id = validate_company_id(company_id) # need to implement this function to check if the company ID exists in the database, and if not, print an error message and ask for the company ID again until a valid one is entered
						if not valid_company_id:
							print(f"Company with ID {company_id} doesn't exist. Please enter a valid Company ID.")
						continue
					except ValueError:
						print("Invalid input. Please enter a valid integer.")
			
			while valid_company_id is True:
						attendees = menuDB.view_attendees(company_id)
						
						attendees = {
							"attendeeName":"Liam Byrne","attendeeDOB":"1990-02-24","sessionTitle":"Scaling Neo4j for Recommendations","speakerName":"Prof. Alan Shaw","sessionDate":"2025-05-12","roomName":"Graph Lab","companyName":"CloudSprint",
							"attendeeName":"Liam Byrne","attendeeDOB":"1990-02-24","sessionTitle":"Customer 360 with SQL","speakerName":"Dr. Niamh Burke","sessionDate": "2025-05-14", "roomName": "Main Hall", "companyName": "CloudSprint",
							"attendeeName":"Cian Roche","attendeeDOB":"1989-09-08","sessionTitle":"Cloud Cost Optimisation","speakerName":"Ruth Collins","sessionDate":"2025-05-14","roomName":"Cloud Suite", "companyName": "CloudSprint",
							"attendeeName":"Cian Roche","attendeeDOB":"1989-09-08","sessionTitle":"FinTech Risk Signals","speakerName":"Marta Silva","sessionDate":"2025-05-13","roomName":"Executive Lounge", "companyName": "CloudSprint",
							"attendeeName":"Evan Brady","attendeeDOB":"1988-12-18","sessionTitle":"Cloud Cost Optimisation","speakerName":"Ruth Collins","sessionDate":"2025-05-14","roomName":"Cloud Suite", "companyName": "CloudSprint"
						}
						
						
						if (attendees != {}):
							print(f"{attendees["companyName"]} Attendees")
							 #for attendee in attendees: # can't get this working, keepss saying "TypeError: string indices must be integers, not 'str'"
							 # print(f"{attendee ["attendeeName"]} | {attendee ["attendeeDOB"]} | {attendee ["sessionTitle"]} | {attendee ["speakerName"]} | {attendee ["sessionDate"]} | {attendee ["roomName"]}  ")
							print(f"{attendees ["attendeeName"]} | {attendees ["attendeeDOB"]} | {attendees ["sessionTitle"]} | {attendees ["speakerName"]} | {attendees ["sessionDate"]} | {attendees ["roomName"]}  ")
							break
							

						elif attendees == {}:
							company_name = menuDB.find_company(company_id)
							print(f"No attendees found for {company_name["companyName"]}")
							no_attendees = True
							break
					

			

			display_menu()
			break
			

		elif choice == "3": # add a new attendee to the database, and return the details of the new attendee
			while True:
					attendee_id = int(input("Enter Attendee's ID number: "))
					attendee_name = input("Enter Attendee's name: ")
					attendee_DOB = input("Enter Attendee's date of birth (yyyy-mm-dd): ")
					
					try:
						attendee_DOB = datetime.strptime(attendee_DOB, '%Y-%m-%d').date()
						#	print(f"{attendee_DOB} is of type {type(attendee_DOB)}")
					except:
						print("Invalid date format. Please enter the date of birth in the format yyyy-mm-dd.")
						attendee_DOB = input("Enter Attendee's date of birth (yyyy-mm-dd): ")

					attendee_gender = input("Enter Attendee's gender: ")
					while attendee_gender not in ["Male", "Female"]:
						print(f"*** ERROR *** Gender must be Male/Female")
						attendee_gender = input("Enter Attendee's gender: ")
					if attendee_gender == "Male":
						gender = 1
					else:
						gender = 2

					valid_company_id = False
					while valid_company_id == False:
						try:
							company_id = int(input("Enter Company ID number: "))
							valid_company_id = validate_company_id(company_id) # need to implement this function to check if the company ID exists in the database, and if not, print an error message and ask for the company ID again until a valid one is entered
							if not valid_company_id:
								print(f"Company with ID {company_id} doesn't exist. Please enter a valid Company ID.")
								continue
						except ValueError:
							print("Invalid input. Please enter a valid integer.")
			

		
					print(f"\nAdd New Attendee")
					print(f"------------------")
					print(f"Attendee ID: {attendee_id}")
					print(f"Attendee Name: {attendee_name}")
					print(f"Attendee DOB: {attendee_DOB}")
					print(f"Attendee Gender: {attendee_gender}")
					print(f"Company ID: {company_id}")
					print(f"\nAttendee successfully added")

					try:
						new_attendee = menuDB.populate_data(attendee_id, attendee_name, attendee_DOB, gender, company_id)
						attendees = menuDB.show_data()
					except Exception as e:
						print("error",e)
					display_menu()		
	

		elif choice == "x":
			break
		else:
			print("in else")
			display_menu()

def validate_company_id(company_id):
	valid_company_id = False
	highest_company_id = 9 # get the highest number of company Id from menuDB and use that to determine the range of valid company Ids
	
	if (company_id > 0) and (company_id <= highest_company_id):
		valid_company_id = True
		return valid_company_id
	elif company_id <= 0 or company_id > highest_company_id:
		valid_company_id = False
		return valid_company_id


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