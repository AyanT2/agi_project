import os
import json
import numpy as np
from scipy.ndimage import label

def find_largest_object(grid):
    grid = np.array(grid)
    if grid.size == 0:
        return []

    max_size = 0
    largest_object_coords = []
    unique_colors = [c for c in np.unique(grid) if c != 0]

    connectivity_structure = np.ones((3, 3))

    for color in unique_colors:
        mask = (grid == color)
        labeled_array, num_features = label(mask, structure=connectivity_structure)

        if num_features > 0:
            object_sizes = [(i, np.sum(labeled_array == i)) for i in range(1, num_features + 1)]
            current_max_label, current_max_size = max(object_sizes, key=lambda item: item[1])

            if current_max_size > max_size:
                max_size = current_max_size
                coords = np.argwhere(labeled_array == current_max_label)
                largest_object_coords = coords.tolist()

    return largest_object_coords

if __name__ == "__main__":
    data_directory = os.path.join('data', 'training')
    output_filename = 'output.txt'
    all_results = []

    try:
        all_files = [f for f in os.listdir(data_directory) if f.endswith('.json')]
        if not all_files:
            print(f"Error: No .json files found in '{data_directory}'.")
            exit()
    except FileNotFoundError:
        print(f"Error: The directory '{data_directory}' was not found.")
        exit()

    num_to_process = 0
    while True:
        try:
            raw_input = input(f"Found {len(all_files)} puzzle files. How many do you want to iterate through? ")
            num_to_process = int(raw_input)
            if 0 < num_to_process <= len(all_files):
                break
            else:
                print(f"Please enter a number between 1 and {len(all_files)}.")
        except ValueError:
            print("Invalid input. Please enter a whole number.")

    files_to_process = all_files[:num_to_process]
    print(f"\n--- Processing the first {len(files_to_process)} files ---")

    for i, filename in enumerate(files_to_process):
        file_path = os.path.join(data_directory, filename)

        print(f"\n==================================================")
        print(f"Processing file {i + 1}/{len(files_to_process)}: {filename}")
        print(f"==================================================")

        try:
            with open(file_path, 'r') as f:
                data = json.load(f)

            puzzle_grid = data['train'][0]['input']
            largest_object = find_largest_object(puzzle_grid)

            output_data = {
                "source_file": file_path.replace('\\', '/'),
                "input_puzzle": puzzle_grid,
                "largest_object_coordinates": largest_object
            }

            all_results.append(output_data)
            print("Successfully processed and added to results.")

        except Exception as e:
            print(f"An unexpected error occurred while processing '{filename}': {e}. Skipping.")

    try:
        with open(output_filename, 'w') as f:
            for result in all_results:
                json_string = json.dumps(result, separators=(',', ':'))
                f.write(json_string + '\n')

        print(f"\n--- All results have been saved to '{output_filename}' ---")
    except IOError as e:
        print(f"Error writing to file '{output_filename}': {e}")

    print("\n--- Script finished ---")