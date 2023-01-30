import json
import random
import string
import argparse

parser = argparse.ArgumentParser(description="some script to obfuscate json files and generate a nametranslation for that file")

# The file containing the JSON to be obfuscated
parser.add_argument("-f", "--file", type=str, help="Path to the input file", required=True)

# Parse the arguments
args = parser.parse_args()

file_name = args.file


# Read the JSON from the file
with open(file_name, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Obfuscate the JSON
name_map = {}

# Function to recursively obfuscate json keys
def obfuscate_json(data):
    if isinstance(data, dict):
        for key in list(data.keys()):
            # Check if the key is in the name map
            if key in name_map:
                # If yes, use the new name
                new_name = name_map[key]
            else:
                # If not, generate a new name
                new_name = ''.join(random.choices(string.ascii_uppercase, k=9))
                name_map[key] = new_name
            # Replace the old key with the new key
            data[new_name] = data.pop(key)
            obfuscate_json(data[new_name])
    elif isinstance(data, list):
        for i in range(len(data)):
            obfuscate_json(data[i])

# Call the function to start recursion
obfuscate_json(data)

# Save the obfuscated JSON to a new file
with open(f'{file_name[:-5]}_obf.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, indent=4)

# Save the name map to a new file
with open(f'{file_name[:-5]}_nametranslation.txt', 'w') as file:
    file.write(json.dumps(name_map, indent=4))

print(f"{file_name} has been obfuscated and saved as '{file_name[:-5]}_obf.json'")
print(f"Nametranslation has been generated and saved as '{file_name[:-5]}_nametranslation.txt'")
