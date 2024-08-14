import json
import glob


def merge_json_files(directory_path):
	merged_data = []
	file_paths = glob.glob(directory_path + '/*.json')
	for path in file_paths:
		with open(path, 'r') as file:
			data = json.load(file)
			print(data)
			merged_data.append(data)
	return merged_data


directory_path = "Anime-dataset-2024/DadosColetados/Details"
output_file = "top_100.json"
merged_data = merge_json_files(directory_path)
with open(output_file, 'w', encoding='utf-8') as outfile:
	json.dump(merged_data, outfile)
print(directory_path)
'''

from os import walk
mypath = "Anime-dataset-2024/DadosColetados/Details"
filenames = next(walk(mypath), (None, None, []))[2]  # [] if no file
print(filenames)
'''