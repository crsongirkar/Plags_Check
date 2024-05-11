# Get the database using the method we defined in pymongo_test_insert file
from Plag_Check.Database.pymongodb import get_database

dbname = get_database()
collection_name = dbname["plag_check"]