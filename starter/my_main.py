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
    "output": "display",
    "return_object": "NEO",
    "start_date": "2020-01-05",
    "end_date": "2020-01-10",
    # "date": "2020-01-01",
    "filename": None,
    "number": 10,
    "filter": ["diameter:>:4"]
}).build_query()

results = NEOSearcher(db).get_objects(query_selectors)
(NEOWriter().write("csv_file", results,
                   output_filename=output_filename))
