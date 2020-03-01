class NearEarthObject(object):
    # Fields
    # Important: id, name, is_potentially_hazardous_asteroid
    # Adding: estimated_diameter_min_kilometers, estimated_diameter_max_kilometers
    # May add in the future if needed: kilometers_per_hour, [OrbitPath] close_approach_date, [OrbitPath] miss_distance_kilometers
    # It should not be the case to deafult them to None since every field shoud have those values, but just because I can I do it
    def __init__(self, **d):
        # if d.get("min_diam") is None or d.get("max_diam") is None:
        #     self.orbits = self.id = self.name = self.is_hazard = self.min_diam = self.max_diam = 1
        #     print(self.min_diam)
        # else:
        self.orbit_to_write = 0
        self.orbits = []
        self.id = d.get("id")
        self.name = d.get("name")
        self.is_hazard = d.get("is_hazard")
        self.min_diam = (d.get("min_diam"))
        self.max_diam = (d.get("max_diam"))

    # def __getitem__(self, key):
    #     if key == "id":
    #         return self.id
    #     if key == "name":
    #         return self.name
    #     if key == "is_hazard":
    #         return self.is_hazard
    #     if key == "min_diam":
    #         return self.min_diam
    #     if key == "max_diam":
    #         return self.max_diam

    def __repr__(self):
        return "Orbits: {}\nId: {}\nName: {}\nIs Hazardous: {}\nMin Diameter: {}\nMax Diameter: {}".format(self.orbits, self.id, self.name, self.is_hazard, self.min_diam, self.max_diam)

    def update_orbits(self, orbit):
        """
        Adds an orbit path information to a Near Earth Object list of orbits

        :param orbit: OrbitPath
        :return: None
        """
        self.orbits.append(orbit)


class OrbitPath(object):
    """
    Object containing data describing a Near Earth Object orbit.
    """
    # id, miss, approch_date, speed

    def __init__(self, **d):
        """
        :param kwargs:    dict of attributes about a given orbit, only a subset of attributes used
        """
        self.id = d.get("id")
        self.miss = (d.get("miss"))
        self.date = d.get("date")
        self.speed = (d.get("speed"))
        # self.speed = (d.get("kilometers_per_hour"))

    def __repr__(self):
        return "\nMiss Distance/Date/Speed = {} | {} | {}".format(self.miss, self.date, self.speed)
