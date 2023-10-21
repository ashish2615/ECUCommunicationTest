""" Run the ECU communication test case. """

from ECUCommunication import TestEcuCommunication


# path to input and output directory
relative_path_for_input_output = "../TestDataAndResult"
input_file_name = "sample.json.txt"
output_file_name = "EcuCommunicationAnalysisResults.csv"
headers_for_output_file = ["MessageName", "SequenceNumber", "Timestamp", "DroppedPackets", "Comment"]


if __name__ == "__main__":

    run_test = TestEcuCommunication.EcuCommunication(
        relative_path_for_input_output,
        input_file_name,
        output_file_name,
        headers_for_output_file
    )
    run_test.test_ecu_communication()
