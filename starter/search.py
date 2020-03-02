from collections import namedtuple, defaultdict
from enum import Enum

from exceptions import UnsupportedFeature
from models import NearEarthObject, OrbitPath

import operator


class DateSearch(Enum):
    """
    Enum representing supported date search on Near Earth Objects.
    """
    between = 'between'
    equals = 'equals'

    @staticmethod
    def list():
        """
        :return: list of string representations of DateSearchType enums
        """
        return list(map(lambda output: output.value, DateSearch))


class Query(object):
    """
    Object representing the desired search query operation to build. The Query uses the Selectors
    to structure the query information into a format the NEOSearcher can use for date search.
    """

    Selectors = namedtuple(
        'Selectors', ['date_search', 'number', 'filters', 'return_object'])
    DateSearch = namedtuple('DateSearch', ['type', 'values'])
    ReturnObjects = {'NEO': NearEarthObject, 'Path': OrbitPath}

    def __init__(self, **d):
        """
        :param kwargs: dict of search query parameters to determine which SearchOperation query to use
        """
        self.date = d.get('date')
        self.end_date = d.get('end_date')
        self.start_date = d.get('start_date')
        self.number = d.get('number')
        self.filter = d.get('filter')
        self.return_object = d.get('return_object')

    def build_query(self):
        """
        Transforms the provided query options, set upon initialization, into a set of Selectors that the NEOSearcher
        can use to perform the appropriate search functionality

        :return: QueryBuild.Selectors namedtuple that translates the dict of query options into a SearchOperation
        """

        if self.date:
            data_search = Query.DateSearch(DateSearch.equals, self.date)
        else:
            data_search = Query.DateSearch(DateSearch.between, [
                self.start_date, self.end_date])

        # number of returned objects after applying the filters
        no_returned_obj = Query.ReturnObjects.get(self.return_object)

        filters = []

        if self.filter:
            options = Filter.create_filter_options(self.filter)
            for id, val in options.items():
                for filter in val:
                    # l = list = splited so 0 field 1 operator 2 value
                    l = filter.split(":")
                    # I would have used Object as the first argument...
                    filters.append(Filter(l[0], id, l[1], l[2]))

        return Query.Selectors(data_search, self.number, filters, no_returned_obj)


class Filter(object):
    """
    Object representing optional filter options to be used in the date search for Near Earth Objects.
    Each filter is one of Filter.Operators provided with a field to filter on a value.
    """
    # Personal wish to filter by id, good for debugging
    Options = {
        "id": "id",
        "is_hazardous": "is_hazard",
        "diameter": ["min_diam", "max_diam"],
        "distance": "miss",
        "date": "date",
        "speed": "speed"
    }

    Operators = {
        "=": operator.eq,
        ">": operator.gt,
        ">=": operator.ge,
        "<": operator.lt,
        "<=": operator.le
    }

    def __init__(self, field, object, operation, value):
        """
        :param field:  str representing field to filter on
        :param field:  str representing object to filter on
        :param operation: str representing filter operation to perform
        :param value: str representing value to filter for
        """
        self.field = field
        self.object = object
        self.operation = operation
        try:
            self.value = float(value)
        except:
            self.value = value

    def __repr__(self):
        return "{}: {} {} {}".format(self.object, self.field, self.operation, self.value)

    @staticmethod
    def create_filter_options(filter_options):
        """
        Class function that transforms filter options raw input into filters

        :param input: list in format ["filter_option:operation:value_of_option", ...]
        :return: defaultdict with key of NearEarthObject or OrbitPath and value of empty list or list of Filters
        """
        ret = defaultdict(list)

        for opt in filter_options:
            filt = opt.split(":")[0]
            operation = opt.split(":")[1]
            if filt == "diameter":
                ret["NEO"].append(opt)
            elif Filter.Options.get(filt) != None:
                if hasattr(NearEarthObject(), Filter.Options.get(filt)):
                    ret["NEO"].append(opt)
                elif hasattr(OrbitPath(), Filter.Options.get(filt)):
                    ret["OP"].append(opt)
            else:
                print("LOG:", "Filter \"{}\" not found!".format(filt))
        return ret

    def apply(self, results, db):
        """
        Function that applies the filter operation onto a set of results

        :param results: List of Near Earth Object results
        :return: filtered list of Near Earth Object results
        """
        # Some explanations:
        # I have branches, 1) if we have to look in the NEO object
        #                       Here 2 more because we have a special field, :diameter:
        #                             1) if the operation is > or >= we have to compare it with estimated_min_diameter
        #                             2) if the operation is < or <= we have to compare it wiht estimated_MAX_diameter
        #                  2) if we have to look in the OrbitPath object
        f = Filter.Options.get(self.field)
        o = Filter.Operators.get(self.operation)
        if self.object == "NEO":
            if self.field == "diameter":
                if self.operation == ">" or self.operation == ">=":
                    return [op for op in results if o(getattr(db[op.id], f[0]), self.value)]
                else:
                    return [op for op in results if o(getattr(db[op.id], f[1]), self.value)]
            else:
                return [op for op in results if o(getattr(db[op.id], f), self.value)]
        else:
            return [op for op in results if o(getattr(op, f), self.value)]
        print("WARNING:", "No filters were applied at all.")


class NEOSearcher(object):
    """
    Object with date search functionality on Near Earth Objects exposed by a generic
    search interface get_objects, which, based on the query specifications, determines
    how to perform the search.
    """

    def __init__(self, db):
        """
        :param db: NEODatabase holding the NearEarthObject instances and their OrbitPath instances
        """
        self.db = db
        # TODO: What kind of an instance variable can we use to connect DateSearch to how we do search?
        # I am not sure of what you mean, I don't need anything else

    def filterByDate(self, l, date_search):
        """
        :param l: List of orbits
        """
        if date_search.type == DateSearch.between:
            return [op for op in l if date_search.values[0] <= op.date <= date_search.values[1]]
        else:
            return [op for op in l if date_search.values == op.date]

    def get_objects(self, query):
        """
        Generic search interface that, depending on the details in the QueryBuilder (query) calls the
        appropriate instance search function, then applys any filters, with distance as the last filter.

        Once any filters provided are applied, return the number of requested objects in the query.return_object
        specified.

        :param query: Query.Selectors object with query information
        :return: Dataset of NearEarthObjects or OrbitalPaths
        """
        # 'Selectors', ['date_search', 'number', 'filters', 'return_object'])
        filters = query[2]

        # Filtering by date
        results = self.filterByDate(self.db.OrbitList, query.date_search)

        for f in filters:
            results = f.apply(results, self.db)

        return results[:query.number]
