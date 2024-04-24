# Export MongoDB Collections to JSON Files

This is a quick python script to list all collections in a MongoDB cluster and allow the user to select which to export to JSON files.

The JSON export omits the _id field, specifically as a workaround for versions that allowed for duplicate _ids.

## Environment
- Python 3.9.6
- Pymongo 3.11.0  (latest version that supports <3.6)
- prompt-toolkit

