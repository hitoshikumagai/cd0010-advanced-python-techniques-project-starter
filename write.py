"""Write a stream of close approaches to CSV or to JSON.

This module exports two functions: `write_to_csv` and `write_to_json`, each of
which accept an `results` stream of close approaches and a path to which to
write the data.

These functions are invoked by the main module with the output of the `limit`
function and the filename supplied by the user at the command line. The file's
extension determines which of these functions is used.

You'll edit this file in Part 4.
"""
import csv
import json
from helpers import datetime_to_str

def write_to_csv(results, filename='output'):
    """Write an iterable of `CloseApproach` objects to a CSV file.

    The precise output specification is in `README.md`. Roughly, each output row
    corresponds to the information in a single close approach from the `results`
    stream and its associated near-Earth object.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    fieldnames = (
        'datetime_utc', 'distance_au', 'velocity_km_s',
        'designation', 'name', 'diameter_km', 'potentially_hazardous'
    )
    #  Write the results to a CSV file, following the specification in the instructions.
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for approach in results:
            # Get the serialized data from both the approach and its NEO
            approach_data = approach.serialize()
            neo_data = approach_data['neo']

            # Create row using serialized data
            row = {
                'datetime_utc': approach_data['datetime_utc'],
                'distance_au': approach_data['distance_au'],
                'velocity_km_s': approach_data['velocity_km_s'],
                'designation': neo_data['designation'],
                'name': neo_data['name'],
                'diameter_km': neo_data['diameter_km'],
                'potentially_hazardous': neo_data['potentially_hazardous']
            }
            writer.writerow(row)


def write_to_json(results, filename='output'):
    """Write an iterable of `CloseApproach` objects to a JSON file.

    The precise output specification is in `README.md`. Roughly, the output is a
    list containing dictionaries, each mapping `CloseApproach` attributes to
    their values and the 'neo' key mapping to a dictionary of the associated
    NEO's attributes.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    #  Write the results to a JSON file, following the specification in the instructions.
    data = []
    for approach in results:
        data.append(approach.serialize())
    
    with open(filename, 'w') as outfile:
        json.dump(data, outfile, indent=2)