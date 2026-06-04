---
title: "Lesson 1.1: Some Example Code"
teaching: 10
exercises: 0
---

:::::::::::::::::::::::::::::::::::::: questions 

- What does a typical research script look like?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Obtain and run example code used for this lesson.
- Examine and identify the sections of the code.

::::::::::::::::::::::::::::::::::::::::::::::::

## Structure of Research Scripts

A research script or notebook often looks like the following:

- get the data
- clean the data up
- perform some analysis, train a model, do some inference
- report the results (plots, tables, save to a file)

Sometimes the code may be a bit mixed up between the sections, for example reporting results and then doing some more analysis, but it's usually possible to organise the code this way.

## Example Code

For this lesson we'll be using some example code available on GitHub, which we'll clone onto our machines using the Bash shell.

So firstly open a Bash shell (via Git Bash in Windows or Terminal on a Mac). Then, on the command line, navigate to where you'd like the example code to reside, and use Git to clone it.

For example, to clone the repository in our home directory, and change our directory to the repository contents:

```bash
cd
git clone https://github.com/
cd refactoring-example
```

You can run the example code:
``` bash
python3 ...
```
which will print out a table of data and create a new JSON file.

Now let's take a look at the code:

``` python
from csv import DictReader
import re
from operator import itemgetter
import json

filename = "data/simplified_coffee_ratings.csv"
country = "Colombia"
min_altitude = 1000

digits = re.compile(r"\d+")
feet_suffixes = {"'", "f", "ft", "feet"}

ratings = [
    "aroma",
    "flavor",
    "aftertaste",
    "acidity",
    "body",
    "balance",
    "uniformity",
    "clean_cup",
    "sweetness",
    "cupper_points",
    "moisture",
]

output_filename = "results.json"


# read the data from the file
with open(filename) as f:
    reader = DictReader(f)
    coffee_data = list(reader)


# clean up the data
for sample in coffee_data:
    # 1. Strip whitespace
    for column, value in sample.items():
        sample[column] = value.strip()

    # 2. Convert measurements to floats
    for column in ratings:
        sample[column] = float(sample[column])

    # 3. clean up altitude data
    altitude = sample["altitude"]

    # - some altitudes give a range
    numbers = [int(value) for value in re.findall(digits, altitude)]

    # - some altitudes are given in feet
    if any(altitude.endswith(suffix) for suffix in feet_suffixes):
        numbers = [int(round(x * 12 * 2.54 / 100, -1)) for x in numbers]

    # - add new columns for min and max altitude
    if len(numbers) == 0:
        sample["min_altitude"] = None
        sample["max_altitude"] = None
    else:
        sample["min_altitude"] = min(numbers)
        sample["max_altitude"] = max(numbers)

    # 4. replace missing values with ""
    for column, value in sample.items():
        if value in {"NA", "-"}:
            sample[column] = ""


# find the Colombian highland coffee
result_data = sorted(
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

# Report results to the terminal
for sample in result_data:
    print(
        "{source:62s} {min_altitude:>5d} {flavor:>5.2f} {cupper_points:>5.2f}".format(
            source=sample["owner"] + ", " + sample["farm_name"], **sample
        )
    )

# Export result data
with open(output_filename, "w") as f:
    json.dump(result_data, f)
```

This is a script that follows the structure introduced in this section:
- it reads in some data from a CSV file
- performs some clean-up:
  - turning strings into numbers
  - untangling altitude data
  - handling missing values
- performs a simple analysis:
  - filters and sorts a subset of the data
- outputs the results:
  - prints to the screen in a tabular format
  - writes to a JSON file
