from database import NEODatabase
import pathlib

PROJECT_ROOT = pathlib.Path(__file__).parent.absolute()
filename = f'{PROJECT_ROOT}/data/neo_data.csv'

db = NEODatabase(filename)
db.load_data()
print("Total NEO in database:", len(db.NEOList.keys()))
print("Total OP in database:", len(db.OrbitList))

orbits = []
for key in db.NEOList:
    if len(db.NEOList[key].orbits) == 8:
        print(db[key]) 