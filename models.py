"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

You'll edit this file in Task 1.
"""
import math
from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """
    
    #  How can you, and should you, change the arguments to this constructor?
    # If you make changes, be sure to update the comments in this file.
    def __init__(self, **info):
        """Create a new `NearEarthObject`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        #  Assign information from the arguments passed to the constructor
        # onto attributes named `designation`, `name`, `diameter`, and `hazardous`.
        # You should coerce these values to their appropriate data type and
        # handle any edge cases, such as a empty name being represented by `None`
        # and a missing diameter being represented by `float('nan')`.
        self.designation = info.get('pdes', 'nan')

        name = info.get('name', '')
        self.name = None if name == '' else name

        # Handle diameter conversion with error handling
        diameter_str = info.get('diameter', '')
        try:
            self.diameter = float(diameter_str) if diameter_str else float('nan')
        except ValueError:
            self.diameter = float('nan')

        # Handle hazardous flag
        self.hazardous = info.get('pha', '').upper() == 'Y'

        # Create an empty initial collection of linked approaches.
        self.approaches = []

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        #  Use self.designation and self.name to build a fullname for this object.
        if self.name is None:
            return self.designation + "(One REALLY BIG fake asteroid)" 
        return self.designation + " (" + self.name + ")"

    def __str__(self):
        """Return `str(self)`."""
        #  Use this object's attributes to return a human-readable string representation.
        # The project instructions include one possibility. Peek at the __repr__
        # method for examples of advanced string formatting.
        hazard_str = "is" if self.hazardous else "is not"
        return f"A NearEarthObject {self.fullname} with a diameter of {self.diameter:.3f} km that {hazard_str} potentially hazardous."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, " \
               f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})"

    def serialize(self):
        """Serialize this NEO into a dictionary for CSV or JSON output."""
        return {
            'designation': self.designation,
            'name': '' if self.name is None else self.name,
            'diameter_km':float('nan') if math.isnan(self.diameter) else float(self.diameter),
            'potentially_hazardous': self.hazardous
        }

class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initially, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """
    
    #  How can you, and should you, change the arguments to this constructor?
    # If you make changes, be sure to update the comments in this file.
    def __init__(self, **info):
        """Create a new `CloseApproach`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        #  Assign information from the arguments passed to the constructor
        # onto attributes named `_designation`, `time`, `distance`, and `velocity`.
        # You should coerce these values to their appropriate data type and handle any edge cases.
        # The `cd_to_datetime` function will be useful.
        self._designation = info.get('des','nan')
        #  Use the cd_to_datetime function for this attribute.
        time_str = info.get('cd', info.get('time', ''))
        self.time = cd_to_datetime(time_str) if time_str else None

        try:
            self.distance = float(info.get('dist', 'nan'))
        except (ValueError, TypeError):
            self.distance = float('nan')
            
        try:
            self.velocity = float(info.get('v_inf', 'nan'))
        except (ValueError, TypeError):
            self.velocity = float('nan')

        # Create an attribute for the referenced NEO, originally None.
        self.neo = None

    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default representation
        includes seconds - significant figures that don't exist in our input
        data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        #  Use this object's `.time` attribute and the `datetime_to_str` function to
        # build a formatted representation of the approach time.
        #  Use self.designation and self.name to build a fullname for this object.
        return datetime_to_str(self.time) if self.time else "Unknown"

    def __str__(self):
        """Return `str(self)`."""
        #  Use this object's attributes to return a human-readable string representation.
        # The project instructions include one possibility. Peek at the __repr__
        # method for examples of advanced string formatting.
        return f"On {self.time_str}, '{self.neo.fullname if self.neo else self._designation}' approaches Earth at a distance of {self.distance:.2f} au and a velocity of {self.velocity:.2f} km/s."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, " \
               f"velocity={self.velocity:.2f}, neo={self.neo!r})"
    def serialize(self):
        """Serialize this close approach into a dictionary for CSV or JSON output."""
        return {
            'datetime_utc': self.time_str,
            'distance_au': self.distance,
            'velocity_km_s': self.velocity,
            'neo': (self.neo.serialize() if self.neo else {
                'designation': self._designation,
                'name': '',  # Empty string for missing name
                'diameter_km': '',  # Empty string for missing diameter
                'potentially_hazardous': False  # # Set to False when NEO is missing
            })
        }