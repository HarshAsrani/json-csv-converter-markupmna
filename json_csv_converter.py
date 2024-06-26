import argparse
import csv
import json

# Set up argument parsing
parser = argparse.ArgumentParser(description='Process a JSON file and create a corresponding CSV file.')
parser.add_argument('json_file', type=str, help='The path to the JSON file to process.')

# Parse the arguments
args = parser.parse_args()

# Function to read and process the JSON file
def process_json(file_path):
    with open(file_path, 'r') as file:
        # Load the JSON content
        data = json.load(file)
        
        # Extract the string associated with the "texts" key
        texts_str = data['texts']
        xpaths_str = data['xpaths']
        highlighted_xpaths_str = data['highlighted_xpaths']
        highlighted_segmented_text_str = data['highlighted_segmented_text']
        tagged_sequence_str = data['tagged_sequence']
        # The string is a representation of a list with escaped quotes,
        # so we replace '\"' with '"' to properly format it,
        # and then remove the leading and trailing square brackets before splitting.
        texts_str_formatted = texts_str.replace('\\"', '"')[1:-1]
        xpaths_str_formatted = xpaths_str.replace('\\"', '"')[1:-1]
        highlighted_xpaths_str_formatted = highlighted_xpaths_str.replace('\\"', '"')[1:-1]
        highlighted_segmented_text_str_formatted = highlighted_segmented_text_str.replace('\\"', '"')[1:-1]
        tagged_sequence_str_formatted = tagged_sequence_str.replace('\\"', '"')[1:-1]

        # Now convert the formatted string back into a list
        text = json.loads(f'[{texts_str_formatted}]')
        xpaths = json.loads(f'[{xpaths_str_formatted}]')
        highlighted_xpaths = json.loads(f'[{highlighted_xpaths_str_formatted}]')
        highlighted_segmented_text = json.loads(f'[{highlighted_segmented_text_str_formatted}]')
        tagged_sequence = json.loads(f'[{tagged_sequence_str_formatted}]')

        # Process highlighted_segmented_text and highlighted_xpaths
        for x in range(len(highlighted_segmented_text)):
            if isinstance(highlighted_segmented_text[x], list):
                if len(highlighted_segmented_text[x]) == 1:
                    highlighted_segmented_text[x] = highlighted_segmented_text[x][0]
                else:
                    highlighted_segmented_text[x] = ''
        for x in range(len(highlighted_xpaths)):
            if tagged_sequence[x] == 'o' and highlighted_xpaths[x] != '':
                highlighted_xpaths[x] = ''
        return text, xpaths, highlighted_xpaths, highlighted_segmented_text, tagged_sequence
        
# Process the JSON file
text, xpaths, highlighted_xpaths, highlighted_segmented_text, tagged_sequence = process_json(args.json_file+".json")

# Determine the CSV file name based on the JSON file name
csv_file_path = args.json_file + '.csv'

# Open the file in write mode and write the data
with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['xpaths', 'text', 'highlighted_xpaths', 'highlighted_segmented_text', 'tagged_sequence'])
    for row in zip(xpaths, text, highlighted_xpaths, highlighted_segmented_text, tagged_sequence):
        writer.writerow(row)

print(f'CSV file "{csv_file_path}" has been created successfully.')
