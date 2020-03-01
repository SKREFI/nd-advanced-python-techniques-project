import csv
from enum import Enum


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

    def write(self, format, data, **d):
        # print("Format:", format)
        # print("Data:", data)
        # print("Dict:", d)
        """
        Generic write interface that, depending on the OutputFormat selected calls the
        appropriate instance write function

        :param format: str representing the OutputFormat
        :param data: collection of NearEarthObject or OrbitPath results
        :param kwargs: Additional attributes used for formatting output e.g. filename
        :return: bool representing if write successful or not
        """
        # format == display
        if format == self.output_format[0]:
            print(data)
            return True
        elif format == self.output_format[1]:  # format == csv_file
            out_file = d.get("output_filename", "data/neo_data_out.csv")
            with open(out_file, 'w') as f:
                fieldnames = ["id", "name", "is_hazardous", "estimated_min_diameter",
                              "estiamted_max_diameter", "miss_distance", "approch_date", "speed"]
                writer = csv.DictWriter(f, fieldnames=fieldnames)

                writer.writeheader()
                for neo in data:
                    writer.writerow({
                        "id": neo.id,
                        "name": neo.name,
                        "is_hazardous": neo.is_hazard,
                        "estimated_min_diameter": neo.min_diam,
                        "estiamted_max_diameter": neo.max_diam,
                        "miss_distance": neo.orbits[neo.orbit_to_write].miss,
                        "approch_date": neo.orbits[neo.orbit_to_write].date,
                        "speed": neo.orbits[neo.orbit_to_write].speed
                    })
                return True
        else:
            print("FATAL: Format file unknown/unspecified")
            return False
