"""
- Read the text file 'HadoopBlurb.txt'.
- Compute the total character count using a dictionary, excluding spaces and special characters.
- Create three different character count dictionaries, assigning characters at random.
- Merge the three dictionaries into one, adding the counts.
- Print the character counts, random character count dictionaries, and merged character count dictionary.
- Perform a test to check if the merged counts match the initial character counts.
"""


import argparse
import random
from typing import Dict, List


def count_characters(file_path: str) -> Dict[str, int]:

    """
    Read a text file and compute total character count using a dictionary.
    Exclude spaces and special characters.
    
    Args:
    - file_path: Path to the text file
    
    Returns:
    - char_counts: Dictionary containing character counts
    """

    # Initialize an empty dictionary
    char_counts: Dict[str, int] = {}

    # Open the file in read mode
    with open(file_path, 'r') as file:
        text = file.read()

    # Iterate over each character in the text
    for char in text:
        # Check if the character is alphanumeric
        if char.isalnum():
            char_counts[char] = char_counts.get(char, 0) + 1 # Increment the count

    return char_counts


def create_random_character_count_dicts(file_path: str) -> List[Dict[str, int]]:

    """
    Create three different character count dictionaries,
    assigning characters at random.
    
    Args:
    - file_path: Path to the text file
    
    Returns:
    - char_counts: List containing three character count dictionaries
    """

    # Initialize a list of three empty dictionaries
    char_counts: List[Dict[str, int]] = [{}, {}, {}]

    # Open the file in read mode
    with open(file_path, 'r') as file:
        text = file.read()

    # Iterate through each character in the text
    for char in text:
        # Check if the character is alphanumeric
        if char.isalnum(): 
            rand_index = random.randint(0, 2) # Randomly select an index
            char_counts[rand_index][char] = char_counts[rand_index].get(char, 0) + 1 # Increment the count

    return char_counts


def merge_character_count_dicts(char_counts_list: List[Dict[str, int]]) -> Dict[str, int]:
    
    """
    Merge three dictionaries into one.
    
    Args:
    - char_counts_list: List containing three character count dictionaries
    
    Returns:
    - merged_counts: Dictionary containing merged character counts
    """

    # Initialize an empty dictionary
    merged_counts: Dict[str, int] = {}

    # Iterate over each dictionary in the list
    for char_dict in char_counts_list:
        # Iterate over each character and its count in the current dictionary
        for char, count in char_dict.items():
            merged_counts[char] = merged_counts.get(char, 0) + count # Add the count to the merged dictionary

    return merged_counts


def test_merge_character_count_dicts(char_counts: Dict[str, int], merged_counts: Dict[str, int]) -> bool:
    
    """
    Test function to check if merged character counts match the character counts.
    
    Args:
    - char_counts: Dictionary containing character counts from count_characters function
    - merged_counts: Dictionary containing merged character counts from merge_character_count_dicts function
    
    Returns:
    - test_result: True if test passes, False otherwise
    """

    # Iterate over each character and its count in the original char_counts dictionary
    for char, count in char_counts.items():
        # Check if the character exists in the merged_counts and if the counts match
        if char not in merged_counts or merged_counts[char] != count:

            return False
    
    print("\n<Part 4>")
    print("Test passed: Merged counts match char counts.")

    return True


def main():
    
    # Set up argument parsing for the file path input
    parser = argparse.ArgumentParser(description = "Character Counting Script")
    parser.add_argument("--file-path", type = str, required = True, help = "Path to the HadoopBlurb.txt file")
    args = parser.parse_args()
    file_path = args.file_path
    
    # Part 1: Count characters from the file
    char_counts: Dict[str, int] = count_characters(file_path)
    max_char = max(char_counts, key = char_counts.get)
    print("\n<Part 1>")
    print(f"Character counts: {char_counts}")
    print(f"Number of unique characters: {len(char_counts)}")
    print(f"Character with the maximum count: '{max_char}' ({char_counts[max_char]} occurrences)")

    # Part 2: Create random character count dictionaries from the file
    random_char_counts: List[Dict[str, int]] = create_random_character_count_dicts(file_path)
    print("\n<Part 2>")
    for i, char_dict in enumerate(random_char_counts, 1):
        print(f"Dict {i}: {char_dict}")

    # Part 3: Merge character count dictionaries
    merged_counts: Dict[str, int] = merge_character_count_dicts(random_char_counts)
    max_merged_char = max(merged_counts, key = merged_counts.get)
    print("\n<Part 3>")
    print(f"Merged character count dictionary: {merged_counts}")
    print(f"Number of unique characters in merged dictionary: {len(merged_counts)}")
    print(f"Character with the maximum count in merged dictionary: '{max_merged_char}' ({merged_counts[max_merged_char]} occurrences)")

    # Part 4: Test if merged counts match original character counts
    test_result: bool = test_merge_character_count_dicts(char_counts, merged_counts)
    if not test_result:
        raise ValueError("Test failed: Merged counts do not match char counts.")

if __name__ == "__main__":
    main()
