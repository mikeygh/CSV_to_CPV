import csv
import sys

class CSVReader(object):
    """CSVReader is a simple class that helps take in a csv file and convert into a list of dictionaries"""

    def __init__(self, filename):
        """The CSVReader intial argument is the file we are going to convert"""
        self.filename = filename

    def get_contents(self):
        """
        Returns a list of dictionaries for every line in the csv.
            With each line the corresponding header is paired with the corresponding element.
        """

        csv_list = []

        # Try accessing the file given, if the csv module has trouble accessing the file
            # or  parsing it , exit the program so the user can verify their input.
        try :
            csv_reader = csv.DictReader(open(self.filename, 'r'))
        except IOError:
            print("Cannot find file , please check input. Exiting..")
            sys.exit()

        # Taking the DictReader object from the csv module, traverse it using the
         #  __iter__ built in method
        for item in csv_reader.__iter__():
            csv_list.append(item)

        # Check to see if the csv_list we are going to return has any data.
            # If it is empty there may have been an issue with the file.
                # raise an IOError.
        if len(csv_list) == 0 :
            raise IOError('File was not a CSV or contained no data')

        return csv_list
