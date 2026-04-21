import menuDB
from datetime import datetime, date  # https://stackoverflow.com/questions/9504356/convert-string-into-date-type-on-python

# Main function

def main():
	# Initialise array
	array = []
	display_menu()

	while True:
		choice = input("Choice: ")

		if choice == "1":
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


		elif choice == "2":
			while True:
				company_invalid = True
				no_attendees = False
				company_id = int(input("\nEnter Company ID number: "))
				valid_company_id = menuDB.view_attendees(company_id)
                
				if company_id > 0 and valid_company_id != ():
					print(f"CloudSprint Attendees")
					print(f"attendee1 | attendee 1 DOB | Session Title | Speaker Name | Date | Room")
					print(f"attendee1 | attendee 2 DOB | Session Title | Speaker Name | Date | Room")
					print(f"attendee1 | attendee 3 DOB | Session Title | Speaker Name | Date | Room")
					print(f"attendee1 | attendee 4 DOB | Session Title | Speaker Name | Date | Room")
					# display_menu()
					break
				elif company_id > 0 and valid_company_id () and not no_attendees:
					print(f"Company with ID {company_id} doesn't exist")
					break
				elif company_id > 0 and valid_company_id != () and no_attendees:
					print(f"No attendees found for Company")
					break
				else:
					print("Invalid input, try again.")

			# print("in 2")
			# print(array)
			# display_menu()

		elif choice == "3":
			attendee_id = int(input("Enter Attendee's ID number: "))
			attendee_name = input("Enter Attendee's name: ")
			attendee_DOB = input("Enter Attendee's date of birth (yyyy-mm-dd): ")
			attendee_DOB = datetime.strptime(attendee_DOB, '%Y-%m-%d').date()
			print(f"{attendee_DOB} is of type {type(attendee_DOB)}")
			attendee_gender = input("Enter Attendee's gender: ")
			if attendee_gender not in ["Male", "Female"]:
				print(f"*** ERROR *** Gender must be Male/Female")
			
			attendee_company_ID = int(input("Enter Attendee's Company ID number: "))
			# Assuming company_invalid is a boolean; fix logic
			#if company_invalid:  # Placeholder; adjust based on actual validation
			#	print(f"*** ERROR *** Company Id: {attendee_company_ID} does not exist")
			#	continue

			print(f"\nAdd New Attendee")
			print(f"------------------")
			print(f"Attendee ID: {attendee_id}")
			print(f"Attendee Name: {attendee_name}")
			print(f"Attendee DOB: {attendee_DOB}")
			print(f"Attendee Gender: {attendee_gender}")
			print(f"Company ID: {attendee_company_ID}")
			print(f"\nAttendee successfully added")
			new_attendee = menuDB.populate_data(attendee_id, attendee_name, attendee_DOB, attendee_gender, attendee_company_ID)
			attendees = menuDB.show_data()

			# find_gt_in_array(array)
			display_menu()

		elif choice == "x":
			break
		else:
			print("in else")
			display_menu()


def view_connected_attendees():
	array = []
	num_enter = int(input("Enter number: "))
	while num_enter != -1:
		array.append(num_enter)
		num_enter = int(input("Enter number: "))
	return array


'''
def find_gt_in_array(array):
	number_entered = int(input("Enter number: "))
	new_array = []
	for num in array:
		if num > number_entered:
			new_array.append(num)

	print(new_array)

'''


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
