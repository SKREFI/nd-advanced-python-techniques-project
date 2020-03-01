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


query_selectors = Query(**{
    "output": "display",
    "return_object": "NEO",
    "date": "2020-01-01",
    "start_date": None,
    "end_date": None,
    "filename": None,
    "number": 10,
    "filter": ["distance:>:74768000"]
}).build_query()

# f = Filter.create_filter_options(["is_hazardous:=:False", "date:=:2020-01-10"])
# print(f)
results = NEOSearcher(db).get_objects(query_selectors)
print(results)
# result = (NEOWriter().write("display", results,
#                             output_filename=output_filename))
