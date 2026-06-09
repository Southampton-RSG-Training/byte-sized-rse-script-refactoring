---
title: "Introduction"
teaching: 15
exercises: 0
---

:::::::::::::::::::::::::::::::::::::: questions 

- What is refactoring?
- When should you refactor your code?
- How do you improve the structure of code without introducing bugs?
- What are the typical patterns of research scripts and notebooks that can be improved?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Understand the basics of refactoring code.
- Recognise common structures of analysis scripts and notebooks.
- Identify these parts and turn them into re-usable functions.
- Identify patterns in functions and group them into classes and objects.
- Understand the importance of testing.

::::::::::::::::::::::::::::::::::::::::::::::::

## Why Refactor?

"Refactoring" is a process where the internal structure of a program or piece of software is modified without changing the external or overall behaviour of the code. Internally the behaviour may change, sometimes dramatically, but users of the code should notice no change: a refactored function should take the same inputs and return the same outputs, for example.

This in contrast with other coding activities, such as adding features and fixing bugs, where the goal is to change the behaviour: either to make the program more correct, or to add useful functionality.  Refactoring is a much more internal and introspective part of software development, and can be hard to justify against the pressures of making code more useful, correct, and applicable in more situations. If no outward behaviour has changed, what is gained?

The answer is that refactoring is *investment* in the code, which should more than repay itself in making ongoing development easier and faster.  When code is grouped logically into modules focused on common concerns it becomes easier to add functionality and identify where problems occur; and perhaps more importantly it becomes easier to test at a granular level.  It also becomes easier to share code, and for collaborators to understand what is happening in a program and why.

But just as with any other investment you do need to think about whether you should spend the effort. Sometimes that effort is repaid immediately: a day spent refactoring before adding new features may repay itself by reducing the development by more than a day.  But sometimes the return is less tangible: a script refactored into a library may be easier for other researchers to use, and so dramatically increase the *impact* of your work even if it doesn't immediately pay-off in terms of effort to do further development.

## What Does Refactoring Involve?

Refactoring typically involves tasks such as:

- thinking and analysing the structure of the code
  - what patterns do you see?
  - how can you change them for the better?
- grouping code thematically into functions, including
  - thinking about what the inputs and outputs of the functions should be
  - restructuring code to call those functions
- grouping related code into re-usable libraries or modules
- grouping functions and data together into classes and objects
- changing an algorithm or library used in a computation

Sometimes it can also involve re-arranging the choices made previously: perhaps the way that functions were grouped into a class previously wasn't quite right and some methods need to be removed and other ones added; or the classes themselves fundametally re-thought.

## Refactoring Confidently

Whenever you change code you run the risk of introducing bugs. Since refactoring involves changing code without changing behaviour to minimise bugs you need to have holistic tests of the code that you are changing: these are typically called *regression tests*, but may take the form of system tests, integration tests or unit tests, depending on the level at which you are refactoring within a codebase.

- before refactoring ensure that you have a way of testing your code
- the tests should be easy to run (ideally just one command) and fast (seconds is better than minutes)
- run your tests after completing every change to ensure that you haven't broken anything
- fix any errors or bugs you have introduced before moving onto the next step

Research scripts and notebooks may not be in a state where they are ready to have formal tests written for them: in this case it is often enough to have a small validation input dataset and a corresponding set of correct outputs that can easily be checked manually. The key is that these should be fast to run and easy to validate.

Depending on the maturity of your code, refactoring might involve breaking some unit tests. If you are refactoring functions with unittests into classes, for example, then you are likely to break the unit tests. Fortunately when refactoring it is usually straightforward to update the tests to use the new code, and doing this helps validate that your choices of how you re-organised your code are good.

## Refactoring Research Scripts

Often when working on new ideas you end up with a script or a notebook that does an analysis that you want, and does it correctly.  In some cases that is good enough: it works, it's replicable, and you don't need to extend it. And that's fine.

Often a research script or notebook looks something like the following:

- get the data
- clean the data up
- the heart of the code: perform some analysis, train a model, do some inference, etc.
- report the results (plots, tables, save to a file)

Sometimes the code may be a bit mixed up between the sections, for example it might report results and then do some more analysis, but it's usually possible to organise the code this way by simply moving the lines around.

Scripts which are in this form is an easy target for a quick refactoring exercise that will dramatically improve the quality and re-usability of your code. You can, incrementally work through the following steps:

- create a *main function* and add *tests*
- turn each of the sections described above into a library of *functions*
- turn groups of functions into *classes*

At the end of each step you will have working code, validated by tests, which is easier to test, easier to modify and adapt in the future, and an improvement on what you had in terms of quality. Of course, you can always stop at the point which feels right for your use case.

::::::::::::::::: keypoints

- refactoring is changing code without changing the inputs and outputs

- refactoring involves thinking about the structure of your code and how you could make it better

- having regression tests allows you to be sure that you don't introduce bugs when refactoring

- research scripts often have a common structure which makes them easy to refactor

- you should refactor code only as much as makes sense based on your plans for use

:::::::::::::::::::::::::::
