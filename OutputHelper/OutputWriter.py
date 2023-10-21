""" This is an output writer class to create an output file."""

import csv
import os
import string


class CsvOutputWriter:
    """ Class to create an output file and add data to it. """

    def __init__(self, relative_path_for_output: string, output_file_name: string, headers: list):
        """
        Initialize the class
        :param relative_path_for_output: Path to store the output file.
        :param output_file_name: output file name.
        :param headers: list of headers for output file.
        """
        self.relative_path_for_output = relative_path_for_output
        self.csv_output_file_name = output_file_name
        self.csv_output_file = os.path.join(self.relative_path_for_output, self.csv_output_file_name)
        self.headers = headers

    def create_output_data_file(self):
        """
        This method creates an output file with headers.
        """
        try:
            with open(self.csv_output_file, "w", newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(self.headers)
        except Exception as e:
            return str(e)

    def append_data_to_csv_output(self, data_to_add: list):
        """
        This method appends test run data to the output data file.
        :param data_to_add: data to be added into the output file.
        """
        with open(self.csv_output_file, "a", newline='') as csv_file:
            csv_output_writer = csv.writer(csv_file)
            csv_output_writer.writerow(data_to_add)
