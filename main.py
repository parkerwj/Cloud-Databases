import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import datetime

# Initialize Firebase Admin SDK with the credential
cred = credentials.Certificate("photo-editing-1cc66-firebase-adminsdk-zhtrb-b42d2a0442.json")
firebase_admin.initialize_app(cred)

# Get a Firestore instance
db = firestore.client()

def main_menu():
    # Display main menu
    print("Main Menu")
    print("1. Add/Update Photographer")
    print("2. Add/Edit/Delete Session")
    print("3. Display Active Sessions")
    print("4. Display Amount Due")
    print("5. Exit")

    # Get user input
    choice = input("Enter your choice: ")

    # Process user input
    if choice == "1":
        photographer_menu()
    elif choice == "2":
        session_menu()
    elif choice == "3":
        display_active_sessions()
    elif choice == "4":
        display_amount_due()
    elif choice == "5":
        exit()
    else:
        print("Invalid choice. Please try again.")
        main_menu()

def photographer_menu():
    # Display photographer menu
    print("Photographer Menu")
    print("1. Add Photographer")
    print("2. Update Photographer")
    print("3. Back to Main Menu")

    # Get user input
    choice = input("Enter your choice: ")

    # Process user input
    if choice == "1":
        add_photographer()
    elif choice == "2":
        update_photographer()
    elif choice == "3":
        main_menu()
    else:
        print("Invalid choice. Please try again.")
        photographer_menu()

def add_photographer():
    # Get input from user
    name = input("Photographer name: ")
    website = input("Photographer website: ")
    email = input("Photographer email: ")

    # Create a new document with auto ID
    doc_ref = db.collection("photographers").document()
    doc_ref.set({
        "name": name,
        "website": website,
        "email": email,
        "sessions": {}
    })

    print("Photographer added.")
    photographer_menu()

def update_photographer():
    # Get input from user
    photographer_id = select_photographer()
    name = input("New photographer name (leave blank if no change): ")
    website = input("New photographer website (leave blank if no change): ")
    email = input("New photographer email (leave blank if no change): ")

    # Update fields in the document
    doc_ref = db.collection("photographers").document(photographer_id)
    data = {}
    if name:
        data["name"] = name
    if website:
        data["website"] = website
    if email:
        data["email"] = email

    if data:
        doc_ref.update(data)

    print("Photographer updated.")
    photographer_menu()

def session_menu():
    # Display session menu
    print("Session Menu")
    print("1. Add Session")
    print("2. Edit Session")
    print("3. Delete Session")
    print("4. Back to Main Menu")

    # Get user input
    choice = input("Enter your choice: ")

    # Process user input
    if choice == "1":
        add_session()
    elif choice == "2":
        edit_session()
    elif choice == "3":
        delete_session()
    elif choice == "4":
        main_menu()
    else:
        print("Invalid choice. Please try again.")
        session_menu()

def add_session():
    # Get input from user
    photographer_id = select_photographer()
    session_type = input("Session type: ")
    is_paid = False if input("Paid (y/n): ") == "n" else True
    session_name = input("Session name: ")
    session_date = input("Session date (YYYY-MM-DD): ")
    delivered_date_input = input("Delivered date (YYYY-MM-DD): ")
    delivered_date = datetime.datetime.strptime(delivered_date_input, "%Y-%m-%d")
    num_images = int(input("Number of images: "))
    price_per_image = float(input("Price per image: "))
    business_days_to_add = 5
    return_date = delivered_date
    for i in range(business_days_to_add):
        # Add one day to the current date
        return_date += datetime.timedelta(days=1)

    # Check if it's a weekend, if yes add necessary days to get to Monday
    while return_date.weekday() in (5, 6):
        return_date += datetime.timedelta(days=1)

    log_transaction(db, f"added {session_type}:{session_name} for the photographer: {photographer_id}, Paid: {is_paid}, Session Date: {session_date}, Delivered Date: {delivered_date}, Images {num_images}, Price Per Image: {price_per_image}, return_date: {return_date}")


    # Compute total cost
    total_cost = num_images * price_per_image

    # Add new session to the photographer's document
    doc_ref = db.collection("photographers").document(photographer_id)
    sessions = doc_ref.get().to_dict()["sessions"]
    new_session_ref = doc_ref.collection("sessions").document()
    new_session_ref.set({
        "session_type": session_type,
        "is_paid": is_paid,
        "session_name": session_name,
        "session_date": session_date,
        "delivered_date": delivered_date,
        "num_images": num_images,
        "price_per_image": price_per_image,
        "return_date": return_date,
        "total_cost": total_cost
    })

    print("Session added.")
    
    session_menu()

def edit_session():
    # Get input from user
    photographer_id = select_photographer()
    session_id = select_session(photographer_id)
    session_ref = db.collection("photographers").document(photographer_id).collection("sessions").document(session_id)
    session_dict = session_ref.get().to_dict()
    print("\nSession Details")
    for key, value in session_dict.items():
        print(f"{key}: {value}")
    print()
    session_type = input("New session type (leave blank if no change): ")
    is_paid = True if input("Paid? (y/n): ") == "y" else False
    session_name = input("New session name (leave blank if no change): ")
    session_date = input("New session date (YYYY-MM-DD) (leave blank if no change): ")
    delivered_date = input("New delivered date (YYYY-MM-DD) (leave blank if no change): ")
    num_images_input = input("New number of images (leave blank if no change): ")
    num_images = int(num_images_input) if num_images_input else None
    price_per_image_input = (input("New price per image (leave blank if no change): "))
    price_per_image = float(price_per_image_input) if price_per_image_input else None
    return_date = input("New return date (YYYY-MM-DD) (leave blank if no change): ")

    # Update fields in the session document
    data = {}
    if session_type:
        data["session_type"] = session_type
    if not is_paid == "":
        data["is_paid"] = is_paid
    if session_name:
        data["session_name"] = session_name
    if session_date:
        data["session_date"] = session_date
    if delivered_date:
        data["delivered_date"] = delivered_date
    if num_images:
        data["num_images"] = num_images
    if price_per_image:
        data["price_per_image"] = price_per_image
    if return_date:
        data["return_date"] = return_date

    if data:
        session_ref.update(data)

    print("Session updated.")
    session_menu()

def delete_session():
    # Get input from user
    photographer_id = select_photographer()
    session_id = select_session(photographer_id)

    # Delete session document and remove reference from the photographer's document
    session_ref = db.collection("photographers").document(photographer_id).collection("sessions").document(session_id)
    session_ref.delete()
    doc_ref = db.collection("photographers").document(photographer_id)
    sessions = doc_ref.get().to_dict()["sessions"]

    doc_ref.update({"sessions": sessions})

    print("Session deleted.")
    session_menu()


def log_transaction(db, message):
    data = {"message": message, "timestamp": firestore.SERVER_TIMESTAMP}
    db.collection("log").add(data)

def display_active_sessions():
    # Get input from user
    photographer_id = select_photographer()

    # Query the sessions collection of the photographer
    query = db.collection("photographers").document(photographer_id).collection("sessions").where("return_date", "==", "")

    # Print out the active sessions
    print(f"\nActive sessions for Photographer {photographer_id}:")
    for doc in query.stream():
        session_dict = doc.to_dict()
        print(f"Session ID: {doc.id}")
        for key, value in session_dict.items():
            if key != "total_cost":
                print(f"{key}: {value}")
        print()

    # Display session menu
    session_menu()

def display_amount_due():
    # Get input from user
    photographer_id = select_photographer()

    # Query the sessions collection of the photographer
    query = db.collection("photographers").document(photographer_id).collection("sessions").where("is_paid", "==", False)

    # Compute total amount due
    total_due = sum([doc.to_dict()["total_cost"] for doc in query.stream()])

    # Print out the total amount due
    print(f"\nAmount Due for Photographer {photographer_id}: ${total_due:.2f}\n")

    # Display main menu
    main_menu()

def select_photographer():
    # Query all photographer documents
    query = db.collection("photographers").stream()

    # Display a list of photographers
    print("\nSelect a Photographer")
    photographer_list = []
    for doc in query:
        photographer_dict = doc.to_dict()
        photographer_list.append(doc.id)
        print(f"{len(photographer_list)} - {photographer_dict['name']}")

    # Get user input
    choice = input("Enter the number of the photographer: ")
    try:
        index = int(choice) - 1
        if 0 <= index < len(photographer_list):
            return photographer_list[index]
        else:
            print("Invalid choice. Please try again.")
            return select_photographer()
    except ValueError:
        print("Invalid choice. Please try again.")
        return select_photographer()

def select_session(photographer_id):
    # Query the sessions collection of the photographer
    query = db.collection("photographers").document(photographer_id).collection("sessions").stream()

    # Display list of sessions
    print("\nSelect a Session")
    session_list = []
    for doc in query:
        session_list.append(doc.id)
        print(f"{len(session_list)} - {doc.to_dict()['session_name']}, {doc.to_dict()['session_date']}")

    # Get user input
    choice = input("Enter the number of the session: ")
    try:
        index = int(choice) - 1
        if 0 <= index < len(session_list):
            return session_list[index]
        else:
            print("Invalid choice. Please try again.")
            return select_session(photographer_id)
    except ValueError:
        print("Invalid choice. Please try again.")
        return select_session(photographer_id)

# Start the program
main_menu()