from csv_reader import CSVReader
from datetime import datetime
from pprint import pprint

class CPV (object):
    """This class  takes a csv of spots and a csv of rotations and returns a dictionary
        of CPV values by each creative or by each rotation by day """

    def __init__(self, spots_filename, rotations_filename):
        self.spots = CSVReader(spots_filename).get_contents()
        self.rotations = CSVReader(rotations_filename).get_contents()

    def cpv_by_creative(self):
        """returns a dictionary with keys being creatives found in the spots csv"""

        # Get a list of creatives by looping through the spots list
        creatives = [spot.get('Creative') for spot in self.spots]

        result_dict = {}

        # For each creative in the creatives loop through each spot in spots
            # and creat a running total of all total_views
                # and total_spent for that particular creative
        for creative in creatives :
            total_viewed = 0
            total_spent = 0
            for spot in self.spots :
                if spot.get('Creative') == creative :
                    total_viewed += int(spot.get('Views'))
                    total_spent += float(spot.get('Spend'))

            # Call calculate_cpv to calculate the cpv
            cpv = self.calculate_cpv(total_spent, total_viewed)
            # Add this information to the result dict
            result_dict[creative] = cpv
        return result_dict

    def calculate_cpv(self, total_spent, total_viewed):
        """Using the formula  CPV = Total_Spent/Total_Viewed
            Return the calculated CPV"""

        # If for some reason our total_spent and total viewed are 0
            # and we have not accounted for that, raise an exception.
        if total_spent == 0 or total_viewed == 0:
            raise Exception("Error calculating CPV")
        return total_spent / total_viewed

    def cpv_by_rotation_by_day(self):
        """returns a dictionary of keys  being the rotations in rotations.csv with values
            equaling a dictionary of CPV per day."""

        result_dict = {}
        # Get a set of each date in the spots list. This will be used to loop through  the total
            # number of days we will need to gather CPVs for.
        dates = set(spot.get('Date') for spot in self.spots)

        # for each rotation loop through each date and call cpv_by_date to get that rotations corresonding data.
        for rotation in self.rotations:
            rotation_name = rotation.get('Name')
            for date in dates:
                # As we build the result dictionary if the result_dict has a specific rotation already,
                    # continue to use but update that value.
                if result_dict.get(rotation_name) :
                    result_dict[rotation_name].update(self.cpv_by_date(date, rotation))
                # Else have that new rotation added to the result_dict
                else :
                    result_dict[rotation_name] = self.cpv_by_date(date, rotation)

        return result_dict

    def cpv_by_date(self, date, rotation):
        """returns a dictionary of the cpv for particular date for a specific rotation"""

        total_viewed = 0
        total_spent = 0

        # Loop through all the spots converting all the time values into datetime objects
        for spot in self.spots:
            strptime_string = '%I:%M %p'
            spot_date = spot.get('Date')
            spot_time = datetime.strptime(spot.get('Time'), strptime_string)
            rotation_start = datetime.strptime(rotation.get('Start'), strptime_string)
            rotation_end = datetime.strptime(rotation.get('End'), strptime_string)

            # determine if the current spot in the loop has time value that lies between the rotation
                # start and end range.
            if date == spot_date:
                if  rotation_start < spot_time < rotation_end:
                    total_viewed += int(spot.get('Views'))
                    total_spent += float(spot.get('Spend'))

        # Check to see if either total_viewed or total_spent is not equal to zero
            # If they are cpv for this date will be 0.
        cpv = 0
        if total_viewed != 0 and total_spent != 0 :
            cpv = self.calculate_cpv(total_spent, total_viewed)

        return {date: cpv}

if __name__ == '__main__':

    cpv = CPV('spots.csv', 'rotations.csv')
    print("CPV By Creative")
    print("---------------")
    pprint(cpv.cpv_by_creative())
    print("\nCPV By Rotation By Day")
    print("--------------------------")
    pprint(cpv.cpv_by_rotation_by_day())