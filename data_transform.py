import argparse
import json
import csv
import sys


def parse_arguments():
    # Set up argument parser and add arguments
    parser = argparse.ArgumentParser(description='Transform JSON data to CSV.')
    parser.add_argument('--inputfile', type=str, required=True, help='The JSON input file.')
    parser.add_argument('--outputfile', type=str, required=True, help='The CSV output file.')
    parser.add_argument('--fields', type=str, required=True, nargs='+', help='Whitespace-separated list of fields to extract.')

    # Parse arguments and return the results
    return parser.parse_args()


def flatten_json(json_data, fields):
    flat_data = []

    def flatten_recursive(obj, field_index, flattened_obj):
        if field_index == len(fields):
            flat_data.append(flattened_obj.copy())
            return

        field = fields[field_index]
        keys = field.split('.')
        value = obj

        # Traverse nested objects using keys
        for key in keys:
            value = value.get(key, {})

        if not value:
            flattened_obj[field] = ""
            flatten_recursive(obj, field_index + 1, flattened_obj)
        elif isinstance(value, list) or (field == "keyword" and isinstance(value, str)):
            if field == "keyword" and isinstance(value, str):
                items = value.split()
            else:
                items = value

            for item in items:
                flattened_obj[field] = item
                flatten_recursive(obj, field_index + 1, flattened_obj)
        else:
            flattened_obj[field] = value
            flatten_recursive(obj, field_index + 1, flattened_obj)

    # Iterate through the JSON objects
    for obj in json_data:
        flatten_recursive(obj, 0, {})

    return flat_data


def main():
    # Parse command line arguments
    args = parse_arguments()

    # Read the JSON input file
    with open(args.inputfile, 'r') as input_file:
        try:
            json_data = json.load(input_file)
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON file: {args.inputfile}", file=sys.stderr)
            sys.exit(1)

    # Get the fields from command line arguments
    fields = args.fields

    # Flatten the JSON data
    flat_data = flatten_json(json_data, fields)

    # Write the flattened data to the CSV output file
    with open(args.outputfile, 'w') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(flat_data)


if __name__ == "__main__":
    main()
