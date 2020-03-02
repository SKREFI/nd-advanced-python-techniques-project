from database import NEODatabase
from writer import NEOWriter
import pathlib
from search import *
# Testing purpose file

PROJECT_ROOT = pathlib.Path(__file__).parent.absolute()
input_filename = f'{PROJECT_ROOT}/data/neo_data.csv'
output_filename = f'{PROJECT_ROOT}/data/neo_data_out.csv'

# First step, load database
db = NEODatabase(input_filename)
db.load_data()

# getting the NEOs with 8 orbits
# obj = []
# for key in db.NEOList:
#     print(db[key])
# if len(db.NEOList[key].orbits) == 8:
#     obj.append(db.NEOList[key])

# "distance:>:74768000"
query_selectors = Query(**{
    "output": "csv_file",
    "start_date": "2020-01-01",
    "end_date": "2020-01-10",
    # "date": "2020-01-02",
    "number": 10,
    "filter": ["is_hazardous:=:False"]
}).build_query()

results = NEOSearcher(db).get_objects(query_selectors)
(NEOWriter().write("display", results, db))
