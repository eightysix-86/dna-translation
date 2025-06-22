from src.utils.codon_table import CodonTable
from src.utils.utils import is_sequence_valid, is_nucleotide_valid

def find_start_codon(sequence: str) -> int:
    """
    Finds the index of the first start codon (ATG) in the DNA sequence.

    Args:
        sequence (str): The DNA sequence to search.

    Returns:
        int: The index of the first start codon, or -1 if not found.
    """
    start_codon = "ATG"
    return sequence.find(start_codon)

def translate_dna_to_protein(sequence: str) -> list[str]:
    """
    Translates a DNA sequence into a protein sequence using the codon table.

    Args:
        sequence (str): The DNA sequence to translate.

    Returns:
        str: The translated protein sequence.
    """
    codon_length = 3
    protein_sequence = []
    start_index = find_start_codon(sequence)
    if start_index == -1:
        return protein_sequence

    if not is_sequence_valid(sequence):
        raise ValueError("Invalid DNA sequence. Only A, T, C, G are allowed.")

    for i in range(start_index, len(sequence) - codon_length + 1, codon_length):
        codon = sequence[i:i + codon_length]
        aa = CodonTable.translate(codon)

        if aa is None:
            raise ValueError(f"Invalid codon '{codon}' found in the sequence.")

        protein_sequence.append(aa)

        if aa == "Stop":
            break

    return protein_sequence

def mutation_change(sequence: str, changes: list[tuple[int, str]]) -> str:
    """
    Applies changes to the DNA sequence.

    Args:
        sequence (str): The original DNA sequence.
        changes (list[tuple[int, str]]): List of tuples where each tuple contains
            an index (1-based) and a nucleotide to change to.

    Returns:
        str: The modified DNA sequence.
    """
    new_seq = sequence
    for pos, nucleotide in changes:
        if 0 <= pos < len(sequence) and is_nucleotide_valid(nucleotide):
            new_seq = new_seq[:pos] + nucleotide.upper() + new_seq[pos + 1:]
        else:
            raise ValueError(f"Position {pos} is out of bounds for the sequence or invalid nucleotide '{nucleotide}'.")
    return new_seq

def mutation_delete(sequence: str, positions: list[int]) -> str:
    """
    Deletes nucleotides from the DNA sequence at specified positions.

    Args:
        sequence (str): The original DNA sequence.
        positions (list[int]): List of positions (1-based) to delete.

    Returns:
        str: The modified DNA sequence.
    """
    if not positions:
        return sequence  # Return the original sequence if no positions are provided

    positions = sorted(set(positions))  # Remove duplicates and sort positions

    if positions[0] < 0:
        raise ValueError(f"Position {positions[0]} is negative. Positions must be non-negative.")

    new_seq = sequence[:positions[0]]
    for i in range(1, len(positions)):
        if 0 <= positions[i] < len(sequence):
            new_seq += sequence[positions[i - 1] + 1:positions[i]]
        else:
            raise ValueError(f"Position {positions[i]} is out of bounds for the sequence.")
    return new_seq + sequence[positions[-1] + 1:]  # Append the rest of the sequence after the last position

def mutation_add(sequence: str, additions: list[tuple[int, str]]) -> str:
    """
    Adds nucleotides to the DNA sequence at specified positions.

    Args:
        sequence (str): The original DNA sequence.
        additions (list[tuple[int, str]]): List of tuples where each tuple contains
            an index (1-based) and a nucleotide to add.

    Returns:
        str: The modified DNA sequence.
    """
    additions = sorted(set(additions), key=lambda x: x[0])  # Remove duplicates and sort by position

    if not additions:
        return sequence

    if additions[0][0] == 0:
        new_seq = additions[0][1].upper()
    elif additions[0][0] < 0:
        raise ValueError(f"Position {additions[0][0]} is negative. Positions must be non-negative.")
    else:
        new_seq = sequence[:additions[0][0]] + additions[0][1].upper()

    for i in range(1, len(additions)):
        if 0 <= additions[i][0] < len(sequence) and is_nucleotide_valid(additions[i][1]):
            new_seq += sequence[additions[i - 1][0]:additions[i][0]] + additions[i][1].upper()
        else:
            raise ValueError(f"Position {additions[i][0]} is out of bounds for the sequence or invalid nucleotide '{additions[i][1]}'.")
    return new_seq + sequence[additions[-1][0]:]  # Append the rest of the sequence after the last position
