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
        "diameter": ["min_diam", "max_diam"],
        "id": "id",
        "speed": "speed",
        "is_hazardous": "is_hazard",
        "distance": "miss",
        "date": "date"
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

    def apply(self, **d):
        db = d.get("database", None)
        neos = d.get("filtered_list", None)
        """
        Function that applies the filter operation onto a set of results

        :param results: List of Near Earth Object results
        :return: filtered list of Near Earth Object results
        """
        filtered_neo = []
        # counter intuitive parameter name (results), more like db or something
        # results.NEOList # the dict in database
        if db == None:
            for neo in neos:
                f = Filter.Options.get(self.field)
                o = Filter.Operators.get(self.operation)
                print(self.value)
                if self.object == "NEO":
                    if self.field == "diameter" and self.operation == ">" or self.operation == ">=":
                        if o(getattr(neo, f[0]), self.value):
                            filtered_neo.append(neo)
                    elif self.field == "diameter" and self.operation == "<" or self.operation == "<=":
                        if o(getattr(neo, f[1]), self.value):
                            filtered_neo.append(neo)
                    elif o(getattr(neo, f), self.value):
                        filtered_neo.append(neo)
                elif self.object == "OP":
                    for i in range(len(neo.orbits)):
                        if o(getattr(neo.orbits[i], f), self.value):
                            neo.orbit_to_write = i
                            filtered_neo.append(neo)
                            continue
            return filtered_neo
        else:
            for id in db.NEOList:
                neo = db[id]
                f = Filter.Options.get(self.field)
                o = Filter.Operators.get(self.operation)
                if self.object == "NEO":
                    if self.field == "diameter" and self.operation == ">" or self.operation == ">=":
                        if o(getattr(neo, f[0]), self.value):
                            filtered_neo.append(neo)
                    elif self.field == "diameter" and self.operation == "<" or self.operation == "<=":
                        if o(getattr(neo, f[1]), self.value):
                            filtered_neo.append(neo)
                    elif o(getattr(neo, f), self.value):
                        filtered_neo.append(neo)
                elif self.object == "OP":
                    op_list = neo.orbits
                    for i in range(len(op_list)):
                        v = getattr(op_list[i], f)
                        if o(v, self.value):
                            neo.orbit_to_write = i
                            filtered_neo.append(neo)
                            # here we continue because we want only uniq neo
                            # so if a neo have multiples orbits which meet
                            # conditions neo will be added multiple times
                            continue
            return filtered_neo


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

    def get_objects(self, query):
        """
        Generic search interface that, depending on the details in the QueryBuilder (query) calls the
        appropriate instance search function, then applys any filters, with distance as the last filter.

        Once any filters provided are applied, return the number of requested objects in the query.return_object
        specified.

        :param query: Query.Selectors object with query information
        :return: Dataset of NearEarthObjects or OrbitalPaths
        """
        # set some defaults in case attributes missing
        # this may not be needed since some may already be a requirement when writing the command
        # but for testing, I will go for it
        n = query.number if query.number != None else 1
        filters = query[2]

        results = []
        if (query.date_search.type == DateSearch.equals):
            f = Filter("date", "OP", "=", query.date_search.values)
            results = f.apply(**{"database": self.db})
        elif (query.date_search.type == DateSearch.between and query.date_search.values[0] and query.date_search.values[1]):
            start_date = query.date_search.values[0]
            end_date = query.date_search.values[1]
            for id in self.db.NEOList:
                for orbit in self.db[id].orbits:
                    if start_date <= orbit.date <= end_date:
                        results.append(self.db[id])
        if len(filters):
            if len(results) == 0:
                results = filters[0].apply(**{"database": self.db})
            else:
                results = filters[0].apply(**{"filtered_list": results})
            for i in range(1, len(filters)):
                results = filters[i].apply(**{"filtered_list": results})

        return results[:query.number] if len(results) > 0 else None
