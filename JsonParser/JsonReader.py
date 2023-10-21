"""Read the Json data file."""

import json
import string


class JsonDataParser:
    """
    Class to read the Json data file and return the json data object.
    """

    def __init__(self, relative_path_for_json_file: string):
        """
        Initialize the class.
        :param relative_path_for_json_file: Path to Json data file
        """
        self.file_name = relative_path_for_json_file

    def get_json_data(self):
        """
        This method reads the JSON data file and return the json data object.
        """
        with open(self.file_name, "r") as data:
            return json.load(data)


