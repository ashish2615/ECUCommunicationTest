This repository contains the coding challenge solution for observing the behaviour of ECUs communication based on cyclic messages send from one ECU to another.
* The challenge requires input data file which is stored in the directory `TestDataAndResults`. The output file of the challenge is also stored in this directory.
* Package `OutputHelper` is used to create an output file with given list of headers. 
  * List of defined headers is `["MessageName", "SequenceNumber", "Timestamp", "DroppedPackets", "Comment"]`
* Package JsonParser is used to read the input Json file and access the Json data object which is then used to access the data for the analysis.
* Package `ECUCommunication` contains the implementation for observing the communication and dropped (or missing) packets during the ECU communication.
* The code can be executed by running the `run_test.py` script in `TestRunner` package.
