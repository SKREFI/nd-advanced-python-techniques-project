import csv
from models import OrbitPath, NearEarthObject


class NEODatabase(object):
    """
    Object to hold Near Earth Objects and their orbits.

    To support optimized date searching, a dict mapping of all orbit date paths to the Near Earth Objects
    recorded on a given day is maintained. Additionally, all unique instances of a Near Earth Object
    are contained in a dict mapping the Near Earth Object name to the NearEarthObject instance.
    """

    def __init__(self, filename):
        """
        :param filename: str representing the pathway of the filename containing the Near Earth Object data
        """
        # TODO: What data structures will be needed to store the NearEarthObjects and OrbitPaths?
        # TODO: Add relevant instance variables for this.
        self.filename = filename
        self.NEOList = {}
        # This is kind of useless, for now, I don't find a use for it, it came by default so
        # I am keeping it in case I need it latter but NEOList is a dictionary which contains every
        # single uniq NEO every single one having a list of orbits, given the data base, after analyzeing it a bit,
        # most of them have only one orbit, the biggest has 8 with the ID: 2164207
        self.OrbitList = []

    def __getitem__(self, key):
        return self.NEOList.get(key)

    def load_data(self, filename=None):
        """
        Loads data from a .csv file, instantiating Near Earth Objects and their OrbitPaths by:
           - Storing a dict of orbit date to list of NearEarthObject instances
           - Storing a dict of the Near Earth Object name to the single instance of NearEarthObject

        :param filename:
        :return:
        """

        if not (filename or self.filename):
            raise Exception('Cannot load data, no filename provided')
        filename = filename or self.filename

        with open(filename, 'r') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')
            # r is a dictionary wich represents each each row in the csv
            for r in reader:
                i = r.get("id")

                neo = {
                    "id": i,
                    "name": r.get("name"),
                    "is_hazard": r["is_potentially_hazardous_asteroid"],
                    "min_diam": float(r.get("estimated_diameter_min_kilometers")),
                    "max_diam": float(r.get("estimated_diameter_max_kilometers"))
                }

                # Mixed up a bit, previously I have build an other dict, now I am calling directly the constructor
                # id miss date speed
                op = OrbitPath(**{
                    "id": i,
                    "miss": float(r["miss_distance_kilometers"]),
                    "date": r["close_approach_date"],
                    "speed": float(r["kilometers_per_second"])
                })
                self.OrbitList.append(op)

                # I am giving the key value of id so I have acces to the object with __getitem__
                # if id of the NEO is already in the DB, add only it's orbit
                if i not in self.NEOList.keys():
                    self.NEOList[i] = NearEarthObject(**neo)
                    self.NEOList[i].orbits.append(op)
                else:
                    self.NEOList[i].orbits.append(op)

        # TODO: Load data from csv file.
        # TODO: Where will the data be stored?

        return None
