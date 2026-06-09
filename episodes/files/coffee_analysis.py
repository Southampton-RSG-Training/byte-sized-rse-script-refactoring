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


def extract_altitudes(sample):
    """Clean up altitude data, adding min and max altitude data."""
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


# read the data from the file
with open(filename) as f:
    reader = DictReader(f)
    coffee_data = list(reader)


# clean up the data
for sample in coffee_data:
    # 1. Strip whitespace
    for column, value in sample.items():
        sample[column] = value.strip()

    # 2. Convert ratings to floats
    for column in ratings:
        sample[column] = float(sample[column])

    # 3. Get altitude information
    extract_altitudes(sample)

    # 4. replace missing values with ""
    for column, value in sample.items():
        if value in {"NA", "-"}:
            sample[column] = ""


# find the Colombian highland coffee
result_data = sorted(
    (
        sample
        for sample in coffee_data
        if (
            sample["country_of_origin"] == country
            and sample["min_altitude"] is not None
            and sample["min_altitude"] >= min_altitude
        )
    ),
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
