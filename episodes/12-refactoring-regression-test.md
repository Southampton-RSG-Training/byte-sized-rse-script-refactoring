---
title: "Creating a Main Function and Tests"
teaching: 10
exercises: 0
---

:::::::::::::::::::::::::::::::::::::: questions 

- How do you get started turning a script into a library?
- How do you test that you changes haven't introduced bugs?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Create a main function.
- Add a test for the main function.

::::::::::::::::::::::::::::::::::::::::::::::::

## Create a Main Function

The first and simplest step you can do towards making a research script re-usable is to wrap it up in a single function.  This can be as simple as wrapping the entire script in a `def main():` and then adding an `if __name__ == '__main__':` that calls the function.  However, with a little thought, you can make your script a simple function that takes parameters that make it more re-usable.

When we look at the example code, we see that we have the following constants in the script:
``` python
filename = "data/simplified_coffee_ratings.csv"
country = "Colombia"
min_altitude = 1000

digits = re.compile(r"\d+")
feet_suffixes = {"'", "f", "ft", "feet"}

ratings = [...]

output_filename = "results.json"
```
Of these the `digits`, `feet_suffixes` and `ratings` constants are things which are likely to remain unchanged, but it is easy to imagine that you might want to run the analysis with different input and output files, and possibly on different countries and minimum altitudes.

So we keep the  `digits`, `feet_suffixes` and `ratings` as module-level constants, but the `filename`, `output_filename`, `country` and `min_altitude` variables make good candidates for the parameters of the main function.  The minimum altitude is less likely to change, so it makes sense to give that a default value.  After this, our script looks like:
``` python
digits = re.compile(r"\d+")
feet_suffixes = {"'", "f", "ft", "feet"}

ratings = [...]

def highland_coffee_report(filename, output_filename, country, min_altitude):
    """Produce a report on coffee suppliers from highland regions."""
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


if __name__ == '__main__':
    highland_coffee_report(
        filename="data/simplified_coffee_ratings.csv",
        output_filename="results.json",
        country="Colombia",
    )
```


### What We've Gained

From this one simple change, our script has become a simple library.  We can now import the code from other scripts, or interactively, to re-use it:
``` python
from highland_coffee_analysis import highland_coffee_report

highland_coffee_report(
    filename="data/simplified_coffee_ratings.csv",
    output_filename="ecuador_results.json",
    country="Ecuador",
)
```

## Writing Tests

We can be reasonably confident that this change hasn't broken the functionality of the script, since we haven't changed any of the core analysis, but our only way of testing this to run the new version of the script and compare the output with what the old version produced.

By creating a function, we've gained is a hook into our code that allows us to write some regression tests.  Regression tests are tests which are designed to ensure that desired behaviour of your code is not changed by any changes you make while developing.  However, at this stage the tests aren't as simple as we might like: these are at the level of *system tests* rather than *unit tests*, and so they have to deal with things like opening and closing of files, inspecting terminal output, and disposing of files once the test is done.

In the sample code we have already written a test for this function:
```python
from contextlib import redirect_stdout
import io
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from highland_coffee_analysis import highland_coffee_report


# Where to look for test input and result data
TEST_DIR = Path(__file__).parent / "test_data"


class TestHighlandCoffeeAnalysis(unittest.TestCase):

    def test_highland_coffee_report(self):
        # Path to input data
        input_file = TEST_DIR / "test_coffee_ratings.csv"

        # Comparison stdout and JSON values.
        with open(TEST_DIR / "test_stdout.txt") as f:
            comparison_stdout = f.read()
        with open(TEST_DIR / "test_output.json") as f:
            comparison_json = json.load(f)

        with TemporaryDirectory() as tmp_dir:
            output_file = Path(tmp_dir) / "results.json"

            # Run the report function, but capture stdout
            out = io.StringIO()
            with redirect_stdout(out):
                highland_coffee_report(input_file, output_file)

            # Test that the output is what we expect
            self.assertEqual(out.getvalue(), comparison_stdout)
            
            # Test the JSON output matches when read back in
            with open(output_file) as f:
                result_json = json.load(f)
            
            self.assertEqual(result_json, comparison_json)
```

This is a bit more complex than some tests you may have seen, but it demonstrates two important techniques for testing the output of research scripts:

- using a `TemporaryDirectory` to create a contained directory for output files which is automatically deleted when it is done (even if there is an error or test failure).

- redirecting standard output using a `StringIO` as a *mock* together with `redirect_stdout`, so that you can validate what is printed to the terminal.

We can run the test code using:
```bash
> python -m unittest tests/test_highland_coffee_analysis.py
```

We can do this after every change we make, and build confidence that out refactoring hasn't introduced any new bugs or unexpected behaviour.

