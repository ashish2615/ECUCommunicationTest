This repository contains the coding challenge solution for observing the behaviour of ECUs communication based on cyclic messages send from one ECU to another ECU.
* The challenge requires input data file which is stored in the directory `TestDataAndResults`. 
  * The output csv file after the test execution is also stored in `TestDataAndResults`.
  * The output file contains five headers as follows:
    * `MessageName`: Name of message.
    * `SequenceNumber`: Message Sequence Number.
    * `Timestamp`: Timestamp corresponding to message sequence observation. 
    * `DroppedPackets`: Number of dropped packets between the message sequence. The number are added iteratively for next message dropped observations.
    * `Comment`: Test run comment for number of packets dropped.
* Package `OutputHelper` is used to create an output file with given list of headers. 
  * List of defined headers is `["MessageName", "SequenceNumber", "Timestamp", "DroppedPackets", "Comment"]`
* Package JsonParser is used to read the input Json file and access the Json data object which is then used to access the data for the analysis.
* Package `ECUCommunication` contains the implementation for observing the communication and dropped (or missing) packets during the ECU communication.
* The code can be executed by running the `run_test.py` script in `TestRunner` package.
