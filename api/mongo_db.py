import os, pymongo
import credentials

def get_database(database):

    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb+srv://{username}:{password}@{cluster}.mongodb.net/{database}".format(
        username = os.getenv('mongo_user'),
        password = os.getenv('mongo_pass'),
        cluster = os.getenv('mongo_cluster'),
        database = database
        )

    # Create a connection using MongoClient
    # print(CONNECTION_STRING)
    client = pymongo.MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client[database]
    
# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":    
    
    # Get the database
    db = get_database('sample_guides')
    print(db)
    test_item = {
        'name': 'Thulcandra',
        'description': 'The Silent Planet'
    }
    table = db['planets']
    table.insert_one(test_item)

    item_details = table.find()
    for item in item_details:
        # This does not give a very readable output
        print(item)

