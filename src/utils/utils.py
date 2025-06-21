"""
General utility functions for the project
"""

def format_sequence(sequence: str) -> str:
    """
    Format a DNA sequence by removing whitespace and converting to uppercase.

    Args:
        sequence (str): The DNA sequence to format.

    Returns:
        str: The formatted DNA sequence.
    """
    sequence = ''.join(sequence.split()).upper()  # Remove whitespace and convert to uppercase
    sequence = sequence.replace('U', 'T')  # change potential U to T
    return sequence

def is_nucleotide_valid(nucleotide: str) -> bool:
    """
    Check if a nucleotide is valid (A, T, C, G).

    Args:
        nucleotide (str): The nucleotide to check.

    Returns:
        bool: True if the nucleotide is valid, False otherwise.
    """
    valid_nucleotides = {'A', 'T', 'C', 'G'}
    return nucleotide.upper() in valid_nucleotides

def is_sequence_valid(sequence: str) -> bool:
    """
    Check if a DNA sequence is valid (contains only A, T, C, G).

    Args:
        sequence (str): The DNA sequence to check.

    Returns:
        bool: True if the sequence is valid, False otherwise.
    """
    return all(is_nucleotide_valid(nucleotide) for nucleotide in sequence.upper())

def get_complementary_sequence(sequence: str) -> str:
    """
    Get the complementary DNA sequence.

    Args:
        sequence (str): The DNA sequence to complement.

    Returns:
        str: The complementary DNA sequence.
    """
    complement = {
        'A': 'T',
        'T': 'A',
        'C': 'G',
        'G': 'C'
    }
    complementary_sequence = ''.join([complement[n] for n in sequence])
    return complementary_sequence

def get_arn_sequence(sequence: str) -> str:
    """
    Get the RNA sequence by replacing T with U.

    Args:
        sequence (str): The DNA sequence to convert.

    Returns:
        str: The RNA sequence.
    """
    sequence = sequence.replace('T', 'U')  # change T to U
    return sequence
