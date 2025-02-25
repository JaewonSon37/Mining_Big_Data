import sys

def run_length_encoding(input_str: str) -> str:

    """
    Perform run-length encoding on the input string.

    Parameters:
        input_str (str): The input string to be encoded.

    Raises:
        TypeError: If the input is not a string.

    Returns:
        str: The run-length encoded string.
    """

    # Ensure the input is a string
    if not isinstance(input_str, str):
        raise TypeError("Input must be a string.")
    
    # Return an empty string if the input is empty
    if not input_str:
        return ""
    
    encoded_segments = [] # List to store encoded segments
    current_char = input_str[0] # Initialize with the first character
    count = 1 # Initialize count for the first character

    # Iterate through the input string starting from the second character
    for char in input_str[1:]:
        if char == current_char:
            count += 1 # Increment count if the character is the same as the previous one
        else:
            encoded_segments.append(f"{current_char},{count}") # Store the current character and its count
            current_char = char # Update current character
            count = 1 # Reset count to 1 for the new character

    # Append the last character and its count to the list
    encoded_segments.append(f"{current_char},{count}")
    
    return ";".join(encoded_segments)

if __name__ == "__main__":
    input_str = sys.stdin.read().strip().strip('"')
    result = run_length_encoding(input_str)
    print(result)
