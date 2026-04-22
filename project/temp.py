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
				#valid_company_id = True
				no_attendees = False
				company_id = int(input("\nEnter Company ID number: "))
				attendees = menuDB.view_attendees(company_id)

				if company_id > 0 and attendees != ():
					print(f"{attendees ["attendeeName"]}")
					print(f"{attendees ["attendeeDOB"]}")
					print(f"{attendees ["sessionTitle"]}")
					print(f"{attendees ["speakerName"]}")
					print(f"{attendees ["roomName"]}")


					'''for attendee in attendees: # can't get this working
						print(f"{attendee ["attendeeName"]} | {attendee ["attendeeDOB"]} | {attendee ["sessionTitle"]} | {attendee ["speakerName"]} | {attendee ["sessionDate"]} | {attendee ["roomName"]}  ")
					'''

					display_menu()
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
'''