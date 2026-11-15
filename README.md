# csv-peek

A quick look at any CSV: row count, and for each column the type, empty cells, unique values, and either min/max/mean/median (numbers) or the most common values (text). One file, standard library only.

## Usage

```
python csv_peek.py data.csv
python csv_peek.py -d ";" data.csv
cat data.csv | python csv_peek.py -
```

Example output:

```
3 rows, 3 columns

name (text): 3 rows, 0 empty, 3 unique
  top: Ada (1), Bo (1), Cy (1)
age (number): 3 rows, 1 empty, 2 unique
  min 30  max 40  mean 35  median 35
city (text): 3 rows, 0 empty, 2 unique
  top: Paris (2), Rome (1)
```

## Notes

- A column counts as a number if every non-empty cell parses as one (thousands commas allowed).
- The whole file is read into memory, so it suits files that fit in RAM.
- Handles a UTF-8 byte order mark.

## Tests

```
python -m unittest discover -s tests -v
```

## License

MIT
