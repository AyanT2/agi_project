Largest Object Finder for JSON Puzzles


Description
-----------

This project contains a Python script designed to process a series of puzzle files in JSON format. For each puzzle, the script identifies the largest connected "object" of a single color within a 2D grid. The coordinates of this largest object are then saved, along with the original puzzle grid, to an output file.

The script is intended to work with puzzle data where 0 is considered the background color and any other integer represents a colored cell. It processes a user-specified number of puzzle files from a designated data directory.


Features
--------

- Parses .json puzzle files from a specified directory.
- Identifies the largest group of connected cells of the same color.
- Connectivity is checked in all 8 directions (including diagonals).
- Handles multiple colors and objects within a single grid.
- Prompts the user to specify how many files to process.
- Outputs results to a .txt file, with each line being a compact JSON object representing one puzzle's result.
- Includes robust error handling for missing files, directories, and invalid user input.


How to Use
----------

1. Project Structure

For the script to run correctly, your project should have the following directory structure:

.
|-- data/
|   `-- training/
|       |-- puzzle1.json
|       |-- puzzle2.json
|       `-- ...
|-- main.py         <-- (Your Python script)
`-- README


Place your .json puzzle files inside the `data/training/` directory.


2. Installation

Before running the script, you need to install the required Python libraries. You can do this using pip and the `requirements.txt` file.

    pip install -r requirements.txt


3. Running the Script

Execute the main Python script from your terminal:

    python main.py

The script will first scan the `data/training/` directory and report the number of puzzle files found. It will then ask you how many of these files you wish to process.

    Found 42 puzzle files. How many do you want to iterate through? 5

Enter a number and press Enter. The script will process the files and save the output.


4. Output

The results will be saved in a file named `output.txt` in the root directory. Each line in this file will be a self-contained JSON object containing:
- source_file: The path to the original puzzle file.
- input_puzzle: The original grid from the puzzle.
- largest_object_coordinates: A list of [row, column] coordinates for the largest object found.


Example `output.txt` line:

{"source_file":"data/training/0a938d7e.json","input_puzzle":[[0,0,5,0],[0,5,5,0],[5,0,5,0]],"largest_object_coordinates":[[0,2],[1,1],[1,2]]}
