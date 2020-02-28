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
        self.OrbitList = []

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
            print(type(reader))
            for r in reader:
                NEO = NearEarthObject(
                    id=r.get("id"),
                    name=r.get("name"),
                    is_hazard=r['is_potentially_hazardous_asteroid'],
                    min_diam=r.get("estimated_diameter_min_kilometers"),
                    max_diam=r.get("estimated_diameter_max_kilometers")
                )
                OP = OrbitPath(
                    id = r.get("id"),
                    miss=r.get("miss_distance_kilometers"),
                    approch_date=r.get("close_approach_date"),
                    speed=r.get("kilometers_per_hour")
                )

                # small = {
                #     "name": r.get("name"),
                #     "is_hazard": r['is_potentially_hazardous_asteroid'],
                #     "min_diam": r.get("estimated_diameter_min_kilometers"),
                #     "max_diam": r.get("estimated_diameter_max_kilometers")
                # }

                # big = {
                #     "id": r.get("id"),
                #     "obj": small
                # }

                # NEO = NearEarthObject(d)

                print(big, end="\n\n")

        # TODO: Load data from csv file.
        # TODO: Where will the data be stored?

        return None
