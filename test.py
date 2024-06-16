def read_file_lines(file_path):
    # Initialize an empty list to store the lines
    lines = []
    
    # Open and read the file
    with open(file_path, 'r') as file:
        # Read all lines
        lines = [line for line in file.readlines()]
    
    return lines

# Define the path to the text file
file_path = 'cleaned_table.txt'

# Call the function and get the lines
lines = read_file_lines(file_path)

# Print the lines without any modification
for line in lines:
    print(line, end='')
