---
title: "Code Blocks to Functions"
teaching: 20
exercises: 0
---

:::::::::::::::::::::::::::::::::::::: questions 

- How do you refactor script sections into functions?
- How do you identify inputs and outputs of the functions?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Refactor the example code as a collection of functions.
- Create a new "main" block for the script.

::::::::::::::::::::::::::::::::::::::::::::::::

## Code Blocks to Functions

Each of the sections sections discussed in the previous section is a natural grouping to take a block and turn it into a function.  This is usually a fairly mechanical process:
- put the function structure around the code block (eg. `def` keyword, indent the block, add docstring)
- work out the inputs and outputs if any
- change the main function

### Refactoring a Code Section

Consider the first block of code that reads the data into a list of dictionaries:

``` python
# read the data from the file
with open(filename) as f:
    reader = DictReader(f)
    coffee_data = list(reader)
```

We start converting it into a function by copying it, indenting and adding a `def` line and turning the comment into a docstring:
``` python
def read_coffee_data_csv():
    """Read the data from the file."""
    with open(filename) as f:
        reader = DictReader(f)
        coffee_data = list(reader)
```

Now we need to determine what the parameters and return values should be. We definitely need to return the coffee data as the result of the function, and it probably makes sense to have the filename as an argument.
``` python
def read_coffee_data_csv(filename):
    """Read the data from the file."""
    with open(filename) as f:
        reader = DictReader(f)
        coffee_data = list(reader)
    return coffee_data
```

At this point we need to add in a line to call the new function with the correct parameters in the place where the code was originally:
``` python
coffee_data = read_coffee_data_csv(filename)
```

### Testing and Committing Your Changes

At this point we have refactored the CSV reading code, but we shouldn't have changed the behaviour. We can verify this by running the test code using:
```bash
> python -m unittest tests/test_highland_coffee_analysis.py
```
The tests should still pass; if they don't you have a bug which needs to be fixed before continuing.

Once you have confirmed that your change is good, this could be a good place to commit your changes with Git.  By doing this you

### Continued Refactoring

We continue with each section of the code, creating functions:
``` python
def clean_coffee_data(coffee_data):
    """Clean up a coffee dataset."""
    for sample in coffee_data:
        # 1. Strip whitespace
        for column, value in sample.items():
            sample[column] = value.strip()

        # 2. Convert measurements to floats
        for column in ratings:
            sample[column] = float(sample[column])

        # 3. get altitude data
        extract_altitude(sample)

        # 4. replace missing values with ""
        for column, value in sample.items():
            if value in {"NA", "-"}:
                sample[column] = ""
```

For the analysis step the parameters should definitely include the coffee data, but the code will be  more useful if we also allow the user to pass additional parameters:
``` python
def find_coffee(coffee_data, country, min_altitude):
    """Find data from a country over a certain altitude."""
    return sorted(
        [
            sample
            for sample in coffee_data
            if (
                sample["country_of_origin"] == country
                and sample["min_altitude"] is not None
                and sample["min_altitude"] >= min_altitude
            )
        ],
        key=itemgetter("flavor", "cupper_points"),
        reverse=True,
    )
```

The output functions are fairly straightforward:
``` python
def print_report(coffee_data):
    """Print a report on a dataset to the terminal."""
    for sample in coffee_data:
        print(
            "{source:62s} {min_altitude:>5d} {flavor:>5.2f} {cupper_points:>5.2f}".format(
                source=sample["owner"] + ", " + sample["farm_name"], **sample
            )
        )


def write_coffee_data_json(coffee_data, path):
    """Export coffee data to JSON."""
    with open(path, "w") as f:
        json.dump(coffee_data, f)
```

The main function should now look like:
``` python
def highland_coffee_report(filename, output_filename, country, min_altitude):
    coffee_data = read_coffee_data_csv(filename)
    clean_coffee_data(coffee_data)
    results = find_coffee(coffee_data, country, min_altitude)
    print_report(results)
    write_coffee_data_json(results, output_filename)
```

As you create each new function, run the tests to make sure that you haven't introduced any errors.

## What We've Gained

We now have a small library of utility functions which may be useful for interactive exploration or to build other scripts.  For example, if we wanted to read in the data and find all the coffee harvested in 2014, we could do something like:
``` python
from highland_coffee_analysis import coffee_data, clean_coffee_data, print_report

coffee_data = read_coffee_data_csv("data/simplified_coffee_ratings.csv")
clean_coffee_data(coffee_data)

coffee_data_2014 = [
    sample for sample in coffee_data if sample["harvest_year"] == "2014"
]
print_report(coffee_data_2014)
```
