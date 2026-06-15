class: title

# Byte-sized RSE: Script Refactoring
## Corran Webster
### Southampton Research Software Group

---
class: title

# Overview

**Introduction:** Refactoring

**Practical activity:** Refactoring a typical research script

## You should have done setup!

---
class: title reverse

# Refactoring
# Introduction

---

# Refactoring

- Refactoring is changing the internal structure of code without changing its overall behaviour
  - internally behaviour may change
  - users of the code shouldn't notice differences
- For example, a refactored function should:
  - take the same inputs
  - return the same outputs
- But it may use a completely different algorithm internally

???

Unlike feature development and bug fixes, refactoring is introspective.  The benefits sometimes can be hard to see compared to spending effort on features or bug fixes.

---

# Why Refactor?

- After refactoring, your code should be:
  - easier to use, to work with and to develop further
  - cleaner and better quality
  - easier to test
- Refactoring is an *investment* in your code
  - before refactoring you should ask whether the return on the investment is worth the effort?

???

Sometimes the pay-off for refactoring is immediate: eg. spending a day refactoring before adding a big new feature may reduce the development effort by more than a day.

But sometimes the return is less tangible: pay off may be in terms of the *impact* of more accessible code, or long-term ease of development.

---

# What Does Refactoring Involve?

- Thinking and analysing the structure of the code
  - finding patterns and changing them for the better
- grouping code thematically into functions
- grouping related code into re-usable libraries or modules
- grouping functions and data together into classes and objects
- changing an algorithm or library used in a computation
- writing tests for the new functions and classes

???

Sometimes it can also involve revisiting the choices made previously when refactoring: usage has shown that you didn't quite get something right

---

# Refactoring Confidently

Changing code risks introducing bugs:

- before refactoring ensure you have *regression tests* for the behaviour you wish to preserve
- the tests should be *easy to run* and *fast*
- run your tests after completing every change
- fix any errors or bugs before moving onto the next step

If there is a problem you want to *fail fast*.

???

Regression tests may take the form of system tests, integration tests or unit tests, depending on the level at which you are refactoring within a codebase.

Easy, fast tests mean you don't lose focus while waiting for feedback on your changes.

Research scripts may not have tests yet: a small validation input set with easy to interpret output may be good enough initially. 

Refactoring may break existing low-level tests, and that's OK. It is often easy to incrementally update existing tests.

---

# Common Research Script Patterns

Research scripts often have a structure like:

.left-column[

- get the data
- clean the data up
- the heart of the code
- report the results

]
.right-column[

``` python
with open("input.csv") as f:
    data = list(DictReader(f))

for sample in data:
    sample["year"] = int(sample["year"])

result = [
    sample for sample in data
    if 2014 <= sample["year"] <= 2020
]

with open("output.json", "w") as f:
    json.dump(f, result)
```

]

Code like this can be quickly and easily refactored.

???

The heart of the code could be anything: perform some analysis, run a simulation, train a model, do some inference, etc.

Sometimes this is good enough, you don't need to refactor.

Sometimes the code may be a bit mixed up between the sections but it's usually possible to organise the code this way by simply moving the lines around.

---

# Refactoring Research Scripts

The refactoring steps often look like:

- create a *main function* and add *tests*
- turn each part of the structure into *functions*
- turn groups of functions into *classes*

At the end of each step you have working, testable code.

???

At the end of the first step, the main function can be used for similar analyses.

At the end of the second step the functions can be re-used (eg. the function for reading the code could be used in another script).

At the end of the last step you have an easy-to-use object that gathers all of the functionality together.

You can always stop at the point which feels right for your use case.

---
class: title reverse

# Refactoring
# Practical Activity

---

# Activity Introduction

- We'll refactor a simple analysis script using the steps we just discussed.
- We'll demonstrate this via live coding.
  - You can use an existing Python installation
  - We'll use a repository with example code.

---
class: title reverse

# Thank you!
# What questions do you have?
