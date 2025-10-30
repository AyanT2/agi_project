# Import necessary libraries
import os  # Used for interacting with the operating system, like file paths
import json  # Used for working with JSON data
import numpy as np  # Used for numerical operations, especially with arrays
from scipy.ndimage import label  # Used for finding and labeling connected components in an array

#Finds the largest connected object of a single color in a 2D grid.
def find_largest_object(grid):
    # Convert the input list of lists to a NumPy array for efficient processing
    grid = np.array(grid)
    # If the grid is empty, there's nothing to process, so return an empty list
    if grid.size == 0:
        return []

    # Initialize variables to keep track of the largest object found so far
    max_size = 0  # Size of the largest object
    largest_object_coords = []  # Coordinates of the largest object

    # Get all unique colors in the grid, excluding 0 (background)
    unique_colors = [c for c in np.unique(grid) if c != 0]

    # Define the connectivity structure for finding objects.
    # This 3x3 array of ones means we consider cells to be connected
    # if they are touching horizontally, vertically, or diagonally.
    connectivity_structure = np.ones((3, 3))

    # Iterate through each unique color to find objects of that color
    for color in unique_colors:
        # Create a boolean mask where True corresponds to cells of the current color
        mask = (grid == color)
        # Use scipy's label function to find all connected components (objects) in the mask
        labeled_array, num_features = label(mask, structure=connectivity_structure)

        # If any objects of the current color were found
        if num_features > 0:
            # Calculate the size of each object found
            object_sizes = [(i, np.sum(labeled_array == i)) for i in range(1, num_features + 1)]
            # Find the object with the largest size for the current color
            current_max_label, current_max_size = max(object_sizes, key=lambda item: item[1])

            # If the largest object of this color is bigger than any object found so far
            if current_max_size > max_size:
                # Update the maximum size
                max_size = current_max_size
                # Get the coordinates of all cells in this new largest object
                coords = np.argwhere(labeled_array == current_max_label)
                # Convert the coordinates to a list and store them
                largest_object_coords = coords.tolist()

    # Return the coordinates of the largest object found across all colors
    return largest_object_coords

# This block of code will only run when the script is executed directly
if __name__ == "__main__":
    # Define the directory where the puzzle data is located and the output filename
    data_directory = os.path.join('data', 'training')
    output_filename = 'output.txt'
    # Initialize a list to store all the results
    all_results = []

    try:
        # Get a list of all files in the data directory that end with .json
        all_files = [f for f in os.listdir(data_directory) if f.endswith('.json')]
        # If no JSON files are found, print an error and exit
        if not all_files:
            print(f"Error: No .json files found in '{data_directory}'.")
            exit()
    except FileNotFoundError:
        # If the data directory doesn't exist, print an error and exit
        print(f"Error: The directory '{data_directory}' was not found.")
        exit()

    # Prompt the user to enter how many files they want to process
    num_to_process = 0
    while True:
        try:
            # Get user input
            raw_input = input(f"Found {len(all_files)} puzzle files. How many do you want to iterate through? ")
            # Convert the input to an integer
            num_to_process = int(raw_input)
            # Check if the number is within a valid range
            if 0 < num_to_process <= len(all_files):
                break  # Exit the loop if the input is valid
            else:
                print(f"Please enter a number between 1 and {len(all_files)}.")
        except ValueError:
            # Handle cases where the input is not a whole number
            print("Invalid input. Please enter a whole number.")

    # Get the subset of files to process based on user input
    files_to_process = all_files[:num_to_process]
    print(f"\n--- Processing the first {len(files_to_process)} files ---")

    # Loop through each file that needs to be processed
    for i, filename in enumerate(files_to_process):
        # Construct the full path to the file
        file_path = os.path.join(data_directory, filename)

        # Print a header for the current file being processed
        print(f"\n==================================================")
        print(f"Processing file {i + 1}/{len(files_to_process)}: {filename}")
        print(f"==================================================")

        try:
            # Open and read the JSON file
            with open(file_path, 'r') as f:
                data = json.load(f)

            # Extract the input grid from the puzzle data
            puzzle_grid = data['train'][0]['input']
            # Call the function to find the largest object in the grid
            largest_object = find_largest_object(puzzle_grid)

            # Create a dictionary to store the results for this file
            output_data = {
                "source_file": file_path.replace('\\', '/'),  # Standardize file path separators
                "input_puzzle": puzzle_grid,
                "largest_object_coordinates": largest_object
            }

            # Add the results for this file to the list of all results
            all_results.append(output_data)
            print("Successfully processed and added to results.")

        except Exception as e:
            # Handle any unexpected errors during file processing
            print(f"An unexpected error occurred while processing '{filename}': {e}. Skipping.")

    # After processing all files, try to save the results to the output file
    try:
        with open(output_filename, 'w') as f:
            # Iterate through each result
            for result in all_results:
                # Convert the result dictionary to a compact JSON string
                json_string = json.dumps(result, separators=(',', ':'))
                # Write the JSON string to the file, followed by a newline
                f.write(json_string + '\n')

        print(f"\n--- All results have been saved to '{output_filename}' ---")
    except IOError as e:
        # Handle errors that may occur while writing to the file
        print(f"Error writing to file '{output_filename}': {e}")

    # Indicate that the script has finished its execution
    print("\n--- Script finished ---")