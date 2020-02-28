class NearEarthObject(object):
    # Fields
    # Important: id, name, is_potentially_hazardous_asteroid
    # Adding: estimated_diameter_min_kilometers, estimated_diameter_max_kilometers
    # May add in the future if needed: kilometers_per_hour, [OrbitPath] close_approach_date, [OrbitPath] miss_distance_kilometers
    # It should not be the case to deafult them to None since every field shoud have those values, but just because I can I do it
    def __init__(self, **d):
        self.orbits = []
        self.id = d.get("id")
        self.name = d.get("name")
        self.is_hazard = d.get("is_hazard")
        self.min_diam = d.get("min_diam")
        self.max_diam = d.get("max_diam")

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

    # TODO: You may be adding instance methods to OrbitPath to help you implement search and output data.
    """

    def __init__(self, **d):
        self.id = d.get("id")
        self.miss = d.get("miss")
        self.approch_date = d.get("approch_date")
        self.speed = d.get("speed")

        """
        :param kwargs:    dict of attributes about a given orbit, only a subset of attributes used
        """
        # TODO: What instance variables will be useful for storing on the Near Earth Object?

    def __repr__(self):
        return "Id: {}\nMiss Distance: {}\nApproach Date: {}\nSpeed: {}".format(self.id, self.miss, self.approch_date, self.speed)
