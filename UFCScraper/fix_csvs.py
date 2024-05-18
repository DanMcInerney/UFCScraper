def remove_duplicate_headers(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    if not lines:
        return  # Exit if the file is empty

    # The first line is the header
    header = lines[0]

    # Create a new list with the header and only those lines that do not match the header
    filtered_lines = [header] + [line for line in lines[1:] if line != header]

    # Write the cleaned data back to the file
    with open(filename, 'w') as file:
        file.writelines(filtered_lines)

remove_duplicate_headers('individuals.csv')
remove_duplicate_headers('competitions.csv')