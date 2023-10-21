This repository contains the coding challenge solution for observing the behaviour of ECUs communication based on cyclic messages send from one ECU to another.
* The challenge requires input data which is contained in the directory `TestDataAndResults`. The output of the challenge is also stored in the same directory.
* Package `OutputHelper` is used to create an output file with given list of headers. List of defined headers is `["MessageName", "SequenceNumber", "Timestamp", "DroppedPackets", "Comment"]`
* Package Jsonparser is used to read the input Json file and access the Json data object which is then used to access the input data.
* Package `ECUCommunication` contains the implementation for observing the communication and dropped (or missing) packets during the communication.
* The code can be executed by running the `run_test.py` script in `TestRunner` package.
