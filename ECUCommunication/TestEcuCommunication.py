""" Test the communication between two ECUs."""

import os
import string

from JsonParser import JsonReader
from OutputHelper.OutputWriter import CsvOutputWriter


class EcuCommunication:
    """Class to test the communication between ECUs."""

    def __init__(self, relative_path_for_input_output_directory: string,
                 input_data_file_name: string,
                 output_data_file_name: string,
                 headers: list):
        """
        Initialize the class.
        :param relative_path_for_input_output_directory: Relative path for input and output files.
        :param input_data_file_name: Name of input data file.
        :param output_data_file_name: Name of output data file.
        :param headers: List of headers for output file.
        """
        self.input_file_path = os.path.join(relative_path_for_input_output_directory, input_data_file_name)
        read_json_file = JsonReader.JsonDataParser(self.input_file_path)
        self.test_data = read_json_file.get_json_data()

        self.data_key = "data"
        self.sequence_counter_key = "SQC_Whl_Msg"
        self.timestamp_key = "timestamp"
        self.expected_sequence_data_keys = (self.data_key, self.timestamp_key)

        self.message_name = None
        self.previous_sequence_timestamp = None
        self.previous_sequence_counter = None
        self.message_sequence_cyclic_time = 20
        self.max_sequence_value = 255
        self.value_not_exist = -1
        self.number_of_packet_dropped = 0
        self.empty_string_value = ""

        self.csv_output_data_file = CsvOutputWriter(relative_path_for_input_output_directory, output_data_file_name,
                                                    headers)
        self.csv_output_data_file.create_output_data_file()

    def test_ecu_communication(self):
        """
        Check if ECUs are communicating and have missing packets.
        """
        # Get message name and corresponding message data from the configs
        self.message_name, message_data = self.get_message_name_and_data()
        # Get the list of all sequences for the given message name.
        list_of_sequences = self.get_list_of_sequences(message_data)

        for sequence in list_of_sequences:
            self.analyze_the_sequence_data(sequence)

    def analyze_the_sequence_data(self, sequence: dict):
        """
        This method analyze the data for each sequence of a given message.
        If there are missing packets log the information into output file.
        :param sequence: Sequence data for a given message.
        """
        # Check if any of the key in message sequence is missing i.e. (data, message_sequence_timestamp)
        if any(key not in sequence.keys() for key in self.expected_sequence_data_keys):
            missing_keys = tuple(set(self.expected_sequence_data_keys) - set(sequence))
            test_result = [self.message_name, self.empty_string_value, self.empty_string_value,
                           self.empty_string_value, f"Message sequence has missing key: {missing_keys}"]
            self.csv_output_data_file.append_data_to_csv_output(test_result)
            return str(KeyError)

        message_sequence_number = self.get_message_sequence_counter(sequence)
        message_sequence_timestamp = self.get_message_sequence_timestamp(sequence)

        # Check if either of message sequence number or message sequence timestamp does value not exist.
        if message_sequence_number == self.value_not_exist or message_sequence_number is None:
            self.number_of_packet_dropped += 1
            self.add_test_results_to_csv(self.message_name, "", str(message_sequence_timestamp),
                                         self.number_of_packet_dropped,
                                         "Message has missing sequence number")
            return
        elif message_sequence_timestamp == self.value_not_exist or message_sequence_timestamp is None:
            self.number_of_packet_dropped += 1
            self.add_test_results_to_csv(self.message_name, str(message_sequence_number), "",
                                         self.number_of_packet_dropped,
                                         "Message sequence has missing timestamp")
            return

        # Set values for previous sequence observations.
        if self.previous_sequence_timestamp is None and self.previous_sequence_counter is None:
            self.previous_sequence_timestamp = message_sequence_timestamp
            self.previous_sequence_counter = message_sequence_number
            return

        # if Sequence has started with max value i.e. 255 set/reset previous sequence counter to -1.
        # -1 is set to meet the condition that consecutive message sequences have a difference of 1.
        if self.previous_sequence_counter == self.max_sequence_value:
            self.previous_sequence_counter = -1

        # Check if current sequence is consecutive to previous sequence
        if message_sequence_number - self.previous_sequence_counter == 1:
            # Calculate the time difference between two consecutive message sequences.
            consecutive_sequence_time_difference = message_sequence_timestamp - self.previous_sequence_timestamp
            if consecutive_sequence_time_difference != 20:
                self.number_of_packet_dropped += 1
                self.add_test_results_to_csv(self.message_name, str(message_sequence_number),
                                             str(message_sequence_timestamp),
                                             self.number_of_packet_dropped,
                                             f"Message sequences are not cyclic. time difference is greater than"
                                             f" {self.message_sequence_cyclic_time}")
        else:
            missing_sequence_numbers = message_sequence_number - self.previous_sequence_counter
            self.number_of_packet_dropped += missing_sequence_numbers
            self.add_test_results_to_csv(self.message_name, self.previous_sequence_counter,
                                         self.previous_sequence_timestamp,
                                         self.number_of_packet_dropped,
                                         f"Message have {missing_sequence_numbers} packets missing between"
                                         f" {self.previous_sequence_counter} and {message_sequence_number} sequence")

        self.previous_sequence_counter = message_sequence_number
        self.previous_sequence_timestamp = message_sequence_timestamp

    def get_message_name_and_data(self) -> tuple:
        """
        Get the data for the given message.
        :return: Message name as key and message data as value.
        """
        for key, value in self.test_data.items():
            return key, value

    def get_message_sequence_counter(self, sequence: dict) -> int:
        """
        This method check for the sequence number of a given message sequence.
        :param sequence: Message sequence to be checked for sequence number.
        :return: int value of message sequence number.
        """
        if self.data_key in sequence:
            if self.sequence_counter_key in sequence[self.data_key]:
                return sequence[self.data_key][self.sequence_counter_key]
        return self.value_not_exist

    def get_message_sequence_timestamp(self, sequence: dict) -> int:
        """
        This method check for the timestamp of a given message sequence.
        :param sequence: Message sequence to be checked for timestamp.
        :return: int value of message sequence timestamp.
        """
        if self.timestamp_key in sequence:
            return sequence[self.timestamp_key]
        return self.value_not_exist

    @staticmethod
    def get_list_of_sequences(message_sequence_data: dict) -> list:
        """
        Get the list of sequences of a message.
        :param message_sequence_data: message data with all sequences.
        :return: list of all sequences of the message.
        """
        for _, value in message_sequence_data.items():
            return value

    def add_test_results_to_csv(self, message_name: string, sequence_number: str, sequence_timestamp: str,
                                packet_dropped_number: int,
                                comment: string):
        """
        This method appends the test case data to the csv output file.
        :param packet_dropped_number:
        :param message_name: Name of message.
        :param sequence_number: Sequence number of the message.
        :param sequence_timestamp: Message sequence timestamp.
        :param packet_dropped_number: Number of packet dropped from the message sequence.
        :param comment: test case status comment.
        """
        test_result = [message_name, sequence_number, sequence_timestamp, packet_dropped_number, comment]
        self.csv_output_data_file.append_data_to_csv_output(test_result)
