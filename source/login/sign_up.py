from database.access_database import MongoDatabase


def sign_up():
    db = MongoDatabase()
    db.connect_database("library_database")
    db.access_collection("users")

    username = input("\nUsername: ")
    email = input("E-mail: ")

    while (
        db.collection.find_one({"username": username}) != None
        or db.collection.find_one({"email": email}) != None
    ):

        print("\nUsername or E-mail already exists.\nTry again!\n")
        username = input("Username: ")
        email = input("E-mail: ")

    passwd = input("Password: ")

    try:
        db.collection.insert_one(
            {
                "username": username,
                "email": email,
                "password": passwd,
                "total_books_issued": 0,
                "currently_issued": [],
                "email_password": None,
            }
        )
    except Exception as e:
        raise Exception("Unable to find the document due to the following error: ", e)

    print("Account created.")
