from database import NEODatabase
from writer import NEOWriter
import pathlib

PROJECT_ROOT = pathlib.Path(__file__).parent.absolute()
input_filename = f'{PROJECT_ROOT}/data/neo_data.csv'
output_filename = f'{PROJECT_ROOT}/data/neo_data_out.csv'

db = NEODatabase(input_filename)
db.load_data()

# obj = []
# for key in db.NEOList:
#     if len(db.NEOList[key].orbits) == 8:
#         obj.append(db.NEOList[key])


obj = []
for key in db.NEOList:
    if db[key].is_hazard == True:
        obj.append(db[key])

writer = NEOWriter()
print(writer.write("csv_file", obj, output_filename=output_filename))
