# Data Transform
This program is designed to transform JSON data into CSV format by flattening nested JSON objects and handling arrays in specific fields. The program takes input from a JSON file and outputs a CSV file with the specified fields.

## Requirements
Python 3.6 or later

## Usage
Run the data transformation script using the following command:

`python3 data_transform.py --inputfile INPUTFILE --outputfile OUTPUTFILE --fields FIELDS [FIELDS ...]`

### Where:

INPUTFILE is the path to the JSON input file.

OUTPUTFILE is the path to the CSV output file.

FIELDS is a whitespace-separated list of fields to extract. Fields can be specified with dot notation to traverse nested objects (e.g., publisher.name).

## Running Tests
The tests for this program can be executed using the following command:

`python3 -m unittest test_data_transform.py`

The test suite includes the following test cases:
test_valid_input_file_and_output_file: Verifies that the program correctly processes a valid input file and produces the expected output file.
test_invalid_input_file: Tests the program's behavior when provided with an invalid JSON input file, ensuring that it produces an error message and exits.
test_missing_fields_in_json_objects: Checks the program's ability to handle JSON objects with missing fields, ensuring that it can still process the data and generate the correct output.
