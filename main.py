import argparse

from src.translator import translate_dna_to_protein, mutation_change, mutation_delete, mutation_add, find_start_codon
from src.utils.utils import is_nucleotide_valid, format_sequence, is_sequence_valid, get_complementary_sequence


def main(args):
    """
    The main function of the script. It processes command line arguments to modify a DNA sequence
    by changing, deleting, or adding mutations, and then translates the modified sequence into a protein.
    """
    # Read the input sequence from standard input
    sequence = format_sequence(args.dna)  # Format the sequence by removing whitespace, converting to uppercase and changing U to T
    if not is_sequence_valid(sequence):
        raise ValueError("Invalid DNA sequence. Only A, T (or U), C, G are allowed.")

    start_idx = args.start if args.start > 0 else 1  # Ensure start index is at least 1
    mutated_sequence = sequence

    # Apply mutations based on command line arguments
    if args.mutation_change:
        changes = args.mutation_change.split()
        changes_pairs = []
        if len(changes) % 2 != 0:
            raise ValueError("Mutation changes must be in pairs of position and nucleotide.")
        for i in range(0, len(changes), 2):
            if not changes[i].isdigit() or not is_nucleotide_valid(changes[i + 1].upper()):
                raise ValueError("Mutation changes must be in the format 'position nucleotide'.")
            if int(changes[i]) < 0:
                raise ValueError(f"Mutation position {changes[i]} is negative.")

            changes_pairs.append((int(changes[i]) - start_idx, changes[i + 1].upper()))  # Convert to zero-based index

        mutated_sequence = mutation_change(mutated_sequence, changes_pairs)

    if args.mutation_del:
        positions = []
        for pos in args.mutation_del.split():
            if not pos.isdigit():
                raise ValueError("Mutation deletions must be numeric positions.")
            if int(pos) < 0:
                raise ValueError(f"Mutation position {pos} is negative.")
            positions.append(int(pos) - start_idx)
        mutated_sequence = mutation_delete(mutated_sequence, positions)

    if args.mutation_add:
        argument = args.mutation_add.split()
        additions = []
        if len(argument) % 2 != 0:
            raise ValueError("Mutation changes must be in pairs of position and nucleotide.")
        for i in range(0, len(argument), 2):
            if not argument[i].isdigit() or not is_nucleotide_valid(argument[i + 1]):
                raise ValueError("Mutation changes must be in the format 'position nucleotide'.")
            if int(argument[i]) < 0:
                raise ValueError(f"Mutation position {argument[i]} is negative.")

            additions.append((int(argument[i]) - start_idx, argument[i + 1].upper()))  # Convert to zero-based index

        mutated_sequence = mutation_add(mutated_sequence, additions)

    # Translate the modified DNA sequence to protein
    if args.strand == "template":
        # If the strand is template, we need to get the complementary sequence
        sequence_temp = sequence
        sequence = get_complementary_sequence(sequence)
        mutated_sequence = get_complementary_sequence(mutated_sequence)
    else:
        sequence_temp = get_complementary_sequence(sequence)

    protein_sequence_init = translate_dna_to_protein(sequence)
    protein_sequence_mutated = translate_dna_to_protein(mutated_sequence)

    translation_start = find_start_codon(sequence)
    protein_size = len(protein_sequence_init) - (1 if protein_sequence_init and protein_sequence_init[-1] == 'Stop' else 0)
    translation_start_mutated = find_start_codon(mutated_sequence)
    protein_size_mutated = len(protein_sequence_mutated) - (1 if protein_sequence_mutated and protein_sequence_mutated[-1] == 'Stop' else 0)

    # Print the results
    print("\n" + 25 *"=" + f" Results for sequence of {len(sequence)} bp " + "=" * 25)
    if not protein_sequence_init:
        print("No protein sequence could be translated from the original DNA sequence.")
        return
    print("\nOriginal DNA Sequence (coding strand): ", ' '.join(sequence[i:i+10] for i in range(0, len(sequence), 10)))
    print("\nOriginal DNA Sequence (template strand): ", ' '.join(sequence_temp[i:i+10] for i in range(0, len(sequence_temp), 10)))
    print("\nInitial Protein Sequence:", '-'.join(protein_sequence_init))
    print(f"Size: {protein_size}")
    if translation_start == -1:
        print("No start codon found in the original sequence.")
    else:
        print(f"Translation starts at position {translation_start + start_idx} for a gene of {protein_size * 3} bp\n")
    if protein_sequence_init[-1] != 'Stop':
        print("Warning: The sequence does not end with a stop codon!\n")

    if not protein_sequence_mutated:
        print("No protein sequence could be translated from the mutated DNA sequence.")
        return
    if mutated_sequence == sequence:
        print("No mutations were applied to the original sequence.")
    else:
        print("\nMutated DNA Sequence: ", ' '.join(mutated_sequence[i:i+10] for i in range(0, len(mutated_sequence), 10)))
        print("\nMutated Protein Sequence:", '-'.join(protein_sequence_mutated))
        print(f"Size: {protein_size_mutated}")
        if translation_start_mutated == -1:
            print("No start codon found in the mutated sequence.")
        else:
            print(f"Translation starts at position {translation_start_mutated + start_idx} for a gene of {protein_size_mutated * 3} bp\n")
        if protein_sequence_mutated[-1] != 'Stop':
            print("Warning: The sequence does not end with a stop codon!\n")

if __name__ == '__main__':
    # Definition of the arguments that can be given through the command line (terminal).
    # If an argument is not given, it will take its default value as defined below.
    parser = argparse.ArgumentParser()

    parser.add_argument('--dna', default="ATG", type=str, help="dna sequence to translate")
    parser.add_argument('--strand', default="coding", type=str, help="coding | template strand")
    parser.add_argument('--start', default=1, type=int, help="start position of the sequence")
    parser.add_argument('--mutation_change', default=None, type=str,
                        help="change mutations in the sequence, "
                             "e.g. '1 A 10 T' to change the first nucleotide to 'A' and 10th one to T")
    parser.add_argument('--mutation_del', default=None, type=str,
                        help="delete mutations in the sequence, e.g. '1 10' to delete nucleotides 1 and 10")
    parser.add_argument('--mutation_add', default=None, type=str,
                        help="add mutations in the sequence, "
                             "e.g. '1 A 10 T' to add 'A' at position 1 and 'T' at position 10")

    args = parser.parse_args()
    main(args)
