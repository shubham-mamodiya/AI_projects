# Heredity

This program calculates the joint probability distribution for individuals having 0, 1, or 2 copies of the Gjb2 gene and whether or not they exhibit a certain trait. It uses probabilistic reasoning to infer the likelihood of gene and trait distribution in a family, given some known data.

## Features

- Loads family data from a CSV file.
- Computes joint probabilities for all possible gene/trait combinations.
- Normalizes probabilities so each distribution sums to 1.
- Prints the probability distribution for each person.

## Usage

1. Place your data file (e.g., `data.csv`) in the same directory.
2. Run the program:
   ```bash
   python heredity.py data.csv
   ```

## Example CSV Format

```csv
name,mother,father,trait
Harry,,,
James,,,
Lily,,,
```

- `trait` should be `1` (has trait), `0` (does not have trait), or blank (unknown).

## Credits

- The logic is inspired by the CS50 AI course.
- This readme.md file was created with the assistance of AI.

---
```# Heredity

This program calculates the joint probability distribution for individuals having 0, 1, or 2 copies of the Gjb2 gene and whether or not they exhibit a certain trait. It uses probabilistic reasoning to infer the likelihood of gene and trait distribution in a family, given some known data.

## Features

- Loads family data from a CSV file.
- Computes joint probabilities for all possible gene/trait combinations.
- Normalizes probabilities so each distribution sums to 1.
- Prints the probability distribution for each person.

## Usage

1. Place your data file (e.g., `data.csv`) in the same directory.
2. Run the program:
   ```bash
   python heredity.py data.csv
   ```

## Example CSV Format

```csv
name,mother,father,trait
Harry,,,
James,,,
Lily,,,
```

- `trait` should be `1` (has trait), `0` (does not have trait), or blank (unknown).

## Credits

- The logic is inspired by the CS50 AI course.
- Github copilot for readme.md file.

---
