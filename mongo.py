import os, pymongo, credentials, pprint


class database:
    # we will only interact with one database with this connection
    database = None

    def __init__(this, database):

        # Provide the mongodb atlas url to connect python to mongodb using pymongo
        CONNECTION_STRING = "mongodb+srv://{username}:{password}@{cluster}.mongodb.net/{database}".format(
            username = os.getenv('mongo_user'),
            password = os.getenv('mongo_pass'),
            cluster = os.getenv('mongo_cluster'),
            database = database
            )

        # Create a connection using MongoClient
        client = pymongo.MongoClient(CONNECTION_STRING)

        # Create the database for our example (we will use the same database throughout the tutorial
        # print(client[database])
        this.database = client[database]

    def connection(this):
        return this.database

    def refresh_token(this, token = None):

        # get/setter for the application refresh access token, which we are storing in mongo
       
        table = this.database['tokens']
        items = table.find({'type':'refresh_token'})

        # there shouldn't be more than one, but we are just looping to consume the db cursor 

        record = None
        for item in items:
            record = item
        
        if token:
            # if token provided, set it in the db
            if record:
                # update existing
                table.update_one({'_id' : record['_id']}, {'$set': {'token':token}})
            else:
                # set a new one
                table.insert_one({'type':'refresh_token', 'token':token})

            return token
        else:
            if record:
                # if token not provided, get it and return it
                return record.get('token')
            else:
                # there was no matching token record in the db
                return False


    
            
# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":    
    
    # Get the database
    db = database('ameritrade_dev')
    # test_item = {
    #     'symbol': 'TSLA',
    #     'description': 'Tesla Motors'
    # }

    table = db.connection()['watchers']

    print(db.refresh_token())
    # table.insert_one(test_item)

    items = table.find({'symbol':'TSLA'})

    pp = pprint.PrettyPrinter(indent=4)

    for item in items:
        # This does not give a very readable output
        pp.pprint(item)
        # table.update_one({'_id' : item['_id']}, {'$set': {'description':'The Garden Take 2'}})


