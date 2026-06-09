---
title: "Functions to Classes"
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

## Functions to Classes

The goal of object oriented programming is to improve code legibility and re-usability by combining information about data structures alongside the code that operates on those data structures.  There's a lot of computer science theory which goes along with that (encapsulation, inhertance, polymorphism, SOLID principles, and so on), but from the pragmatic point of view for research code, writing classes can make your code easier to use by resucing the cognitive load on your users (including "future you").

A deeper dive into OOP is outside the scope of this class, and we're going to assume a basic level of familiarity with Python's OOP features.

Often you'll notice patterns of functions which take the same parameter or similar related parameters. For example, most of the functions we have written take a `coffee_data` variable which is a list of sample dictionaries:
``` python
def clean_coffee_data(coffee_data): ...

def find_coffee(coffee_data, country, min_altitude): ...

def print_report(coffee_data): ...

def write_coffee_data_json(coffee_data, path): ...
```
When we see patterns like this, it's a good sign that a class may be appropriate where the common parameters become attributes of the class and the functions become methods.

This transformation is again, fairly mechanical. First we create the structure of the class with an `__init__` method that takes the common parameters and assigns them as attributes:
``` python
class CoffeeData:

    def __init__(self, coffee_data):
        self.coffee_data = list(coffee_data)
```
We can then take each of our functions and transform them into methods.  The common parameters are replaced by `self` in the function signature, and then in the body of the method they are replaced by the attribute:
``` python
class CoffeeData:

    ...

    def print_report(self):
        """Print a report on a dataset to the terminal."""
        for sample in self.coffee_data:
            print(
                "{source:62s} {min_altitude:>5d} {flavor:>5.2f} {cupper_points:>5.2f}".format(
                    source=sample["owner"] + ", " + sample["farm_name"], **sample
                )
            )
```

The `find_coffee` function is a little bit more complex: not only does it take some additonal arguments, but it should create and return a new `CoffeeData` instance with the results of the analysis:
``` python
class CoffeeData:

    ...

    def find_coffee(self, country, min_altitude):
        """Find data from a country over a certain altitude."""
        coffee_data_list = sorted(
            (
                sample
                for sample in self.coffee_data
                if (
                    sample["country_of_origin"] == country
                    and sample["min_altitude"] is not None
                    and sample["min_altitude"] >= min_altitude
                )
            ),
            key=itemgetter("flavor", "cupper_points"),
            reverse=True,
        )
        return CoffeeData(coffee_data_list)
```

We can also refactor the `read_coffee_data_csv` file to be a *class method*. This is a useful Python idiom for providing alternative constructors for a class:
``` python
class CoffeeData:
    ...

    @classmethod
    def read_csv(cls, filename):
        with open(filename) as f:
            reader = DictReader(f)
            coffee_data = cls(reader)
        return coffee_data
```

Finally, in our main function, we need to create the instance of the class, and then repace function calls with method calls:
``` python
def highland_coffee_report(filename, output_filename, country, min_altitude):
    coffee_data = CoffeeData.read_csv(filename)
    coffee_data.clean_data()
    results = coffee_data.find_coffee(country, min_altitude)
    results.print_report()
    results.write_coffee_data_json(output_filename)
```

::::::::::::::::: callout

## What we've gained

We now have a single object that encapsulates the data that we want to work with, which can simplify and improve the readability of our code, and make it easier to work with interactively.

Taking the example from the previous section, if we wanted to read in the data and find all the coffee harvested in 2014, we could do something like:
``` python
from highland_coffee_analysis import CoffeeData

coffee_data = CoffeeData.read_csv("data/simplified_coffee_ratings.csv")
coffee_data.clean_data()

coffee_data_2014 = CoffeeData(
    sample for sample in coffee_data.coffee_data if sample["harvest_year"] == "2014"
)
coffee_data_2014.print_report()
```
Compared to the function version, we've simplified the imports and the method calls

### Alternative Approaches and Extensions

There are some choices here that we could make differently, such as perhaps calling `clean_data` as part of `read_csv`. These sorts of decisions depend on external factors such as whether we get data in other formats (such as Excel spreadsheets) which need similar cleaning, or whether sometimes we get csv files which *don't* need cleaning.

Similarly, if you are experienced with Python OOP, there are some additional tweaks that you can add to make the class even easier to use, such as making it a [`Sequence`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence) which allows you to use it in `for` loops and to index into it like a list or tuple:

``` python
from collections.abc import Sequence

class CoffeeData(Sequence):
    ...

    def __len__(self):
        return len(self.coffee_data)
    
    def __iter__(self):
        return iter(self.coffee_data)
```

One thing to keep in mind is that software is very plastic: if it turns out you made the wrong choice it's easy to re-write to make a better choice later once you have more experience with the problems and use-cases.

:::::::::::::::::::::::::

## Testing

Again, our top-level regression test should still work perfectly: we haven't changed *what* the code does, just *how* it does it.

This is a logical end-point in refactoring, so now would be a good time to write unit tests for the class and each of the methods to gain confidence that the code is behaving as expected when there are corner-cases.

::::::::::::::::: keypoints

- objects and classes group data and the functions that operate on the data together

- functions with common parameters are natural targets to become methods on a class and the parameters become attributes

- input processing functions may make good class methods in Python

- classes are often easier for users to use as they reduce the number of imports and the complexity of function calls

- when you have created the class the regression tests should still pass

- when you have finished refactoring it is a good idea to write unit tests for the refactored code

:::::::::::::::::::::::::::
