# connect to mongodb://10.0.0.3:27019 and list dbs

from pymongo import MongoClient
import os
import json
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.shortcuts import checkboxlist_dialog
from prompt_toolkit.styles import Style

client = MongoClient('mongodb://10.0.0.3:27019')
db = client.admin
dbs = client.list_database_names()

# list all databases in the cluster with document count


def list_colls():
    for db in dbs:
        # list each collection in the db along with the number of documents
        print(f"{db}")
        colls = client[db].list_collection_names()
        for coll in colls:
            name = coll
            size = client[db][coll].count_documents({})
            print(f"  {name} ({size})")

# import test data from the import folder


def import_test_data():
    for file in os.listdir("import"):
        if file.endswith(".json"):
            db, coll = file.split(".")[0:2]
            print(f"Importing {file} into {db}.{coll}")
            with open(f"import/{file}", "r") as f:
                data = json.load(f)
                for document in data:
                    # Transform the _id field into a string
                    document['_id'] = document['_id']['$oid']
                client[db][coll].insert_many(data)

# gui to select collections to export to json


def select_collections():
    # Get a list of all collections in all databases
    all_collections = []
    for db in dbs:
        colls = client[db].list_collection_names()
        for coll in colls:
            all_collections.append(f"{db}.{coll}")

    # Create a checkbox list dialog
    dialog = checkboxlist_dialog(
        title="Select collections",
        text="Use SPACE to toggle selection and ENTER to confirm:",
        values=[(c, c) for c in all_collections],
        style=Style.from_dict({
            'dialog': 'bg:#88ff88',
            'button': 'bg:#ffffff #000000',
            'dialog.body': 'bg:#00aa00 #ffffff',
            'dialog shadow': 'bg:#00aa00',
            'dialog border': 'bg:#00aa00 #ffffff bold',
        })
    )

    # Show the dialog and return the selected collections
    return dialog.run()


colls = select_collections()

# create a json file in export folder for each selected collection without the _id field
for coll in colls:
    db, coll = coll.split(".")
    print(f"Exporting {db}.{coll}")
    data = list(client[db][coll].find({}, {"_id": 0}))
    with open(f"export/{db}.{coll}.json", "w") as f:
        json.dump(data, f, indent=4)


client.close()
