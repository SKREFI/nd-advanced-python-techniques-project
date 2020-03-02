import csv
from enum import Enum
import TableIt


class OutputFormat(Enum):
    """
    Enum representing supported output formatting options for search results.
    """
    display = 'display'
    csv_file = 'csv_file'

    @staticmethod
    def list():
        """
        :return: list of string representations of OutputFormat enums
        """
        return list(map(lambda output: output.value, OutputFormat))


class NEOWriter(object):
    """
    Python object use to write the results from supported output formatting options.
    """

    def __init__(self):
        self.output_format = OutputFormat.list()

    def write(self, format, data, db, **d):
        """
        Generic write interface that, depending on the OutputFormat selected calls the
        appropriate instance write function

        :param format: str representing the OutputFormat
        :param data: collection of NearEarthObject or OrbitPath results
        :param kwargs: Additional attributes used for formatting output e.g. filename
        :return: bool representing if write successful or not
        """

        def printTable():
            table = []
            table.append(["id", "name", "is_hazardous", "estimated_min_diameter",
                          "estimated_max_diameter", 'miss_distance', "approch_date", "speed"])
            for op in data:
                small_list = [op.id, db[op.id].name, db[op.id].is_hazard,
                              db[op.id].min_diam, db[op.id].max_diam, op.miss, op.date, op.speed]
                small_list = [str(item) for item in small_list]
                table.append(small_list)
            TableIt.printTable(table, useFieldNames=True)
            print("Found {} elements.".format(len(data)))

        def myNormalPrint():
            # A bit spaced up so it is a bit easier to read
            print("id,     name,       is_hazardous, estimated_min_diameter, estimated_max_diameter, miss_distance,     approch_date, speed")
            for op in data:
                print("{},{},{},        {},           {},           {}, {},   {}".format(
                    op.id, db[op.id].name, db[op.id].is_hazard, db[op.id].min_diam, db[op.id].max_diam, op.miss, op.date, op.speed))
            print("Found {} elements.".format(len(data)))

        # format == display
        try:
            if format == self.output_format[0]:
                # this is what I used previously, in case there is a problme with me using the TableIt module
                # myNormalPrint()
                printTable()
                return True
            elif format == self.output_format[1]:  # format == csv_file
                out_file = d.get("output_filename", "data/neo_data_out.csv")
                with open(out_file, 'w') as f:
                    fieldnames = ["id", "name", "is_hazardous", "estimated_min_diameter",
                                  "estimated_max_diameter", "miss_distance", "approch_date", "speed"]
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    for op in data:
                        writer.writerow({
                            "id": op.id,
                            "name": db[op.id].name,
                            "is_hazardous": db[op.id].is_hazard,
                            "estimated_min_diameter": db[op.id].min_diam,
                            "estimated_max_diameter": db[op.id].max_diam,
                            "miss_distance": op.miss,
                            "approch_date": op.date,
                            "speed": op.speed
                        })
                    return True
            else:
                print("FATAL: Output format unknown/unspecified")
                return False
        except:
            return False
