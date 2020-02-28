from database import NEODatabase
import pathlib

PROJECT_ROOT = pathlib.Path(__file__).parent.absolute()
filename = f'{PROJECT_ROOT}/data/neo_data.csv'

db = NEODatabase(filename)
db.load_data()
