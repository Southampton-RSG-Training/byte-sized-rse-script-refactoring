from contextlib import redirect_stdout
import io
import json
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
                highland_coffee_report(input_file, output_file, "Colombia")

            # Test that the output is what we expect
            self.assertEqual(out.getvalue(), comparison_stdout)
            
            # Test the JSON output matches when read back in
            with open(output_file) as f:
                result_json = json.load(f)
            
            self.assertEqual(result_json, comparison_json)
