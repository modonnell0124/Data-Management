import csv
import json
import argparse

def csv_to_json(csv_file, json_file):
    try:
        # Read the CSV
        with open(csv_file, mode='r') as file:
            reader = csv.DictReader(file)  # Reads as a dictionary
            data = [row for row in reader]

        # Write to JSON
        with open(json_file, mode='w') as file:
            json.dump(data, file, indent=4)

        print(f"Successfully converted '{csv_file}' to '{json_file}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Set up CLI argument parsing
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert a CSV file to JSON.")
    parser.add_argument("csv_file", help="Path to the input CSV file.")
    parser.add_argument("json_file", help="Path to the output JSON file.")

    args = parser.parse_args()

    # Call the conversion function
    csv_to_json(args.csv_file, args.json_file)
