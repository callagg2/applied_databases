# Main function

def main():
	# Initialise array
	array = []
	display_menu()
	
	while True:
		choice = input("Choice: ")
		
		if (choice == "1"):
			speaker_name = input("\nEnter speaker name: ")
			print(f"Sessions Details For: {speaker_name}")
			print(f"---------------------")
			if "dr" in speaker_name:
				#print(f"Sessions Details For: {speaker_name}")
				#print(f"---------------------\n")
				print(f"{speaker_name} | Session Title | Room")
				display_menu()
			else:
				print(f"No speakers found of that name")
				display_menu()
            
            #print("in 1")
            #array = fill_array()
            
	
		elif (choice == "2"):
			while True:
				company_invalid = True
				no_attendees = False
				company_id = int(input("\nEnter Company ID number: "))
				if (company_id > 0) and (company_invalid) is False:
					print(f"CloudSprint Attendees")
					print(f"attendee1 | attendee 1 DOB | Session Title | Speaker Name | Date | Room")
					print(f"attendee1 | attendee 2 DOB | Session Title | Speaker Name | Date | Room")
					print(f"attendee1 | attendee 3 DOB | Session Title | Speaker Name | Date | Room")
					print(f"attendee1 | attendee 4 DOB | Session Title | Speaker Name | Date | Room")
				    #display_menu()
				elif ((company_id > 0) and (company_invalid) is True and (no_attendees)) is False:
					print(f"Company with ID {company_id} doesn't exist")
				elif (((company_id > 0) and (company_invalid) is True) and (no_attendees)) is True:
					print(f"No attendees found for Company")
		
		
					
				    #print(f"No speakers found of that name")
	                #display_menu()
            
            #print("in 2")
			#print(array)
			#display_menu()
		elif (choice == "3"):
			attendee_id = int(input("Enter Attendee's ID number: "))
			attendee_name = (input("Enter Attendee's name: "))
			attendee_DOB = (input("Enter Attendee's date of birth (yyyy-mm-dd): "))
			attendee_gender = (input("Enter Attendee's gender: "))
			attendee_company_ID = int(input("Enter Attendee's Company ID number: "))
			print(f"\nAdd New Attendee")
			print(f"------------------")
			print(f"Attendee ID: {attendee_id}")
			print(f"Attendee Name: {attendee_name}")
			print(f"Attendee DOB: {attendee_DOB}")
			print(f"Attendee Gender: {attendee_gender}")
			print(f"Company ID: {attendee_company_ID}")
			print(f"\nAttendee successfully added")
            #print("in 3")
			#find_gt_in_array(array)
			display_menu()
		elif (choice == "x"):
			break;
		else:
			print("in else")
			#display_menu()
			
'''	
def fill_array():
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
	
	print (new_array)

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
    print("x - Exit appliation")

if __name__ == "__main__":
	# execute only if run as a script 
	main()
