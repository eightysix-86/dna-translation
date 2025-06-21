# DNA Sequence Translator

## Overview
This program processes DNA sequences, applies mutations, and translates them into protein sequences. It supports various operations such as formatting DNA sequences, validating them, applying mutations (change, delete, add), and translating DNA to protein using a codon table.

## Features
- Format DNA sequences (remove whitespace, convert to uppercase, replace `U` with `T`).
- Validate DNA sequences (ensure they contain only valid nucleotides: `A`, `T`, `C`, `G`).
- Apply mutations:
  - **Change**: Replace nucleotides at specific positions.
  - **Delete**: Remove nucleotides at specific positions.
  - **Add**: Insert nucleotides at specific positions.
- Translate DNA sequences into protein sequences using a codon table.
- Handle both coding and template strands.

## Requirements
- Python 3.8 or higher
- Required Python libraries (if any)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/eightysix-86/dna-translation.git
   cd <repository-directory>

2. Ensure Python is installed on your system.

## Usage
### Terminal Commands
Run the program using the following command:

```bash
python main.py --dna <sequence> [options]
```

### Arguments
- `--dna`: The DNA sequence to process (default: `ATG`).
- `--strand`: Specify the strand type (`coding` or `template`) (default: `coding`).
- `--start`: Start index of the sequence (default: `1`- indexed).
- `--mutation_change`: Apply mutations to change nucleotides. Format: `<position nucleotide>`. Example with `1 C 4 T`:
"ATGCGT" -> "**C**TG**T**GT"
- `--mutation_del`: Apply mutations to delete nucleotides. Format: `<position>`. Example with `1 5`:
"ATGCGT" -> "~~A~~TGC~~G~~T" = "TGCT"
- `--mutation_add`: Apply mutations to add nucleotides. Format: `<position nucleotide>`. Example with `1 A 4 T`:
"ATGCGT" -> "**A**ATG**T**CGT"

### Examples
#### Basic Translation
```bash
python main.py --dna "ATGCGT"
```
```
Original DNA Sequence:  ATGCGT
Initial Protein Sequence: Met-Arg
Size: 2

Warning: The original sequence does not end with a stop codon!

No mutations were applied to the original sequence.
```

#### Apply Change Mutation
```bash
python main.py --dna "ATGCGT" --mutation_change "13 G 14 A"
```
```
Original DNA Sequence:  ATGCGT
Initial Protein Sequence: Met-Arg
Size: 2

Warning: The sequence does not end with a stop codon!

Mutated DNA Sequence:  ATGAGT
Mutated Protein Sequence: Met-Ser
Size: 2

Warning: The sequence does not end with a stop codon!
```

#### Apply Deletion Mutation
```bash
python main.py --dna "ATGCGT" --mutation_del "5"
```
```
Original DNA Sequence:  ATGCGT
Initial Protein Sequence: Met-Arg
Size: 2

Warning: The sequence does not end with a stop codon!

Mutated DNA Sequence:  ATGCT
Mutated Protein Sequence: Met
Size: 1

Warning: The sequence does not end with a stop codon!   
```

#### Apply Addition Mutation
```bash
python main.py --dna "ATGCGT" --mutation_add "4 A 5 G"
```
```
Original DNA Sequence:  ATGCGT
Initial Protein Sequence: Met-Arg
Size: 2

Warning: The sequence does not end with a stop codon!

Mutated DNA Sequence:  ATGACGGT
Mutated Protein Sequence: Met-Thr
Size: 2

Warning: The sequence does not end with a stop codon!
```

#### Apply Multiple Mutations
```bash
python main.py --dna "ATGCGT" --mutation_change "3 G 4 A" --mutation_del "5" --mutation_add "5 G"
```
```
Original DNA Sequence:  ATGCGT
Initial Protein Sequence: Met-Arg
Size: 2

Warning: The sequence does not end with a stop codon!

Mutated DNA Sequence:  ATGAGT
Mutated Protein Sequence: Met-Ser
Size: 2

Warning: The sequence does not end with a stop codon!
```

#### Use Different Indexing
```bash
python main.py --dna "ATGCGT" --start "11" --mutation_change "13 G 14 A"
```
```
Original DNA Sequence:  ATGCGT
Initial Protein Sequence: Met-Arg
Size: 2

Warning: The sequence does not end with a stop codon!

Mutated DNA Sequence:  ATGAGT
Mutated Protein Sequence: Met-Ser
Size: 2

Warning: The sequence does not end with a stop codon!
```

#### Template Strand
```bash
python main.py --dna "TACCGT" --strand "template"
```
```
Coding strand: ATGGCA

Original DNA Sequence:  ATGGCA
Initial Protein Sequence: Met-Ala
Size: 2

Warning: The sequence does not end with a stop codon!

No mutations were applied to the original sequence.
```

### Output
The program prints:
- Original DNA sequence
- Initial protein sequence
- Mutated DNA sequence (if mutations are applied)
- Mutated protein sequence

## Testing
Run unit tests to verify functionality:
```bash
python -m unittest discover tests
```

## License
This project is licensed under the GNU License. See the `LICENSE` file for details.
