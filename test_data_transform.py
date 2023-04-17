import os
import unittest
import json
import csv
import subprocess

class TestDataTransform(unittest.TestCase):
    def setUp(self):
        self.test_input_file = "test_input.json"
        self.valid_output_file = "my.csv"
        self.invalid_input_file = "invalid.json"
        self.missing_fields_input_file = "missing_fields.json"
        self.empty_input_file = "empty.json"
        self.nonexistent_input_file = "nonexistent.json"
        self.existing_output_file = "existing.csv"
        self.fields = ["modified", "publisher.name", "publisher.subOrganizationOf.name", "contactPoint.fn", "keyword"]

        valid_data = [
            {
                "modified": "2017-05-15",
                "publisher": {
                    "name": "General Services Administration",
                    "subOrganizationOf": {
                        "name": "General Services Administration"
                    }
                },
                "contactPoint": {
                    "fn": "Mick Harris"
                },
                "keyword": [
                    "Assignment Plan", "CIO", "Common Baseline", "FITARA", "GSA IT", "Implementation Plan"
                ]
            }
        ]

        # Create a test input JSON file
        with open(self.test_input_file, "w") as f:
            json.dump(valid_data, f)

        # Create an invalid JSON file
        with open(self.invalid_input_file, "w") as f:
            f.write("This is not valid JSON")

        # Create a JSON file with missing fields
        missing_fields_data = [
            {
                "modified": "2017-05-15",
                "publisher": {
                    "name": "General Services Administration"
                },
                "contactPoint": {
                    "fn": "Mick Harris"
                },
                "keyword": [
                    "Assignment Plan", "CIO", "Common Baseline", "FITARA", "GSA IT", "Implementation Plan"
                ]
            },
            {
                "modified": "2022-03-30T15:14:53.668Z",
                "publisher": {
                    "name": "General Services Administration",
                    "subOrganizationOf": {
                        "name": "General Services Administration"
                    }
                },
                "contactPoint": {
                    "fn": "Mick Harris"
                },
                "keyword": [
                    "Assignment Plan"
                ]
            }
        ]

        with open(self.missing_fields_input_file, "w") as f:
            json.dump(missing_fields_data, f)

        # Create an empty JSON file
        with open(self.empty_input_file, "w") as f:
            json.dump([], f)

               # Create a valid output file for comparison
        with open(self.valid_output_file, "w") as f:
            writer = csv.DictWriter(f, fieldnames=self.fields)
            writer.writeheader()
            writer.writerow({"modified": "2017-05-15", "publisher.name": "General Services Administration",
                            "publisher.subOrganizationOf.name": "General Services Administration", "contactPoint.fn": "Mick Harris", "keyword": "Assignment Plan"})
            writer.writerow({"modified": "2017-05-15", "publisher.name": "General Services Administration",
                            "publisher.subOrganizationOf.name": "General Services Administration", "contactPoint.fn": "Mick Harris", "keyword": "CIO"})
            writer.writerow({"modified": "2017-05-15", "publisher.name": "General Services Administration",
                            "publisher.subOrganizationOf.name": "General Services Administration", "contactPoint.fn": "Mick Harris", "keyword": "Common Baseline"})
            writer.writerow({"modified": "2017-05-15", "publisher.name": "General Services Administration",
                            "publisher.subOrganizationOf.name": "General Services Administration", "contactPoint.fn": "Mick Harris", "keyword": "FITARA"})
            writer.writerow({"modified": "2017-05-15", "publisher.name": "General Services Administration",
                            "publisher.subOrganizationOf.name": "General Services Administration", "contactPoint.fn": "Mick Harris", "keyword": "GSA IT"})
            writer.writerow({"modified": "2017-05-15", "publisher.name": "General Services Administration",
                            "publisher.subOrganizationOf.name": "General Services Administration", "contactPoint.fn": "Mick Harris", "keyword": "Implementation Plan"})

        # Create an existing output file
        with open(self.existing_output_file, "w") as f:
            f.write("Existing output file")

    def tearDown(self):
        # Delete the output files after each test
        os.remove(self.test_input_file)
        os.remove(self.valid_output_file)
        os.remove(self.invalid_input_file)
        os.remove(self.missing_fields_input_file)
        os.remove(self.empty_input_file)
        os.remove(self.existing_output_file)


    def test_valid_input_file_and_output_file(self):
        # Test with valid input file and output file
        subprocess.run(["python3", "data_transform.py", "--inputFile", self.missing_fields_input_file, "--outputFile", "test_output.csv", "--fields", *self.fields], check=True)
        with open(self.valid_output_file) as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        self.assertEqual(len(rows), 6)
        self.assertEqual(rows[0]["keyword"], "Assignment Plan")

    def test_invalid_input_file(self):
        # Test with invalid input file
        result = subprocess.run(["python3", "data_transform.py", "--inputFile", self.invalid_input_file, "--outputFile", "test_output.csv", "--fields", "modified", "publisher.name", "publisher.subOrganizationOf.name", "contactPoint.fn", "keyword"], capture_output=True, text=True)
        self.assertIn("Error: Invalid JSON file:", result.stderr)

    def test_missing_fields_in_json_objects(self):
        # Test with missing fields in JSON objects
        subprocess.run(["python3", "data_transform.py", "--inputFile", self.missing_fields_input_file, "--outputFile", "test_output.csv", "--fields", *self.fields], check=True)
        with open("test_output.csv") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        self.assertEqual(len(rows), 7)
        self.assertEqual(rows[0]["keyword"], "Assignment Plan")
        self.assertEqual(rows[1]["publisher.name"], "General Services Administration")
        self.assertEqual(rows[2]["publisher.subOrganizationOf.name"], "")
        self.assertEqual(rows[3]["contactPoint.fn"], "Mick Harris")
        self.assertEqual(rows[4]["keyword"], "GSA IT")
        self.assertEqual(rows[5]["modified"], "2017-05-15")
        self.assertEqual(rows[6]["modified"], "2022-03-30T15:14:53.668Z")

