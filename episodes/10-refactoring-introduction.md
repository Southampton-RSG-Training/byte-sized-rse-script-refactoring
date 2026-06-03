---
title: "Lesson 1: Refactoring Research Scripts"
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

This session provides a look at *refactoring* code, the process of improving the structure of code without changing the overall behaviour.  In particular we will look at the common patterns found in code written in analysis scripts and notebooks.  With thought and care you can turn these into re-usable libraries that can form the core of multiple analysis libraries.

## Why Refactor?

"Refactoring" is a process where the internal structure of a program or piece of software is modified without changing the external or overall behaviour of the code. Internally the behaviour may change, sometimes dramatically, but users of the code should notice no change: a refactored function should take the same inputs and return the same outputs, for example.

This in contrast with other coding activities, such as adding features and fixing bugs, where the goal is to change the behaviour: either to make the program more correct, or to add useful functionality.  Refactoring is a much more internal and introspective part of software development, and can be hard to justify against the pressures of making code more useful, correct, and applicable in more situations. If no outward behaviour has changed, what is gained?

The answer is that refactoring is *investment* in the code, which should more than repay itself in making ongoing development easier and faster.  When code is grouped logically into modules focused on common concerns it becomes easier to add functionality and identify where problems occur; and perhaps more importantly it becomes easier to test at a granular level.  It also becomes easier to share code, and for collaborators to understand what is happening in a program and why.

But just as with any other investment you do need to think about whether you should spend the effort. Sometimes that effort is immediate: a day spent refactoring before adding new features may repay itself by reducing the development by more than a day.  But sometimes the return is less tangible: a script refactored into a library may be easier for other researchers to use, and so dramatically increase the *impact* of your work even if it doesn't immediately pay-off in terms of effort to do further development.

## What Does Refactoring Involve?

Refactoring typically involves a number of steps:

- thinking and analysing the structure of the code - what patterns do you see and how can you change them for the better?
- grouping code blocks thematically into functions
- thinking about what the inputs and outputs of the functions should be
- restructuring code to call those functions
- grouping related code into re-usable libraries or modules
- grouping functions and data together into classes and objects
- changing an algorithm or library used in a computation

Sometimes it can also involve re-arranging the choices made previously: perhaps the way that functions were grouped into a class previously wasn't quite right and some methods need to be removed and other ones added; or the classes themselves fundametally re-thought.

## Refactoring Confidently

Whenever you change code you run the risk of introducing bugs. Since refactoring involves changing code without changing behaviour to minimise bugs you need to have holistic tests of the code that you are changing: depending on the level of the code you are working with these may be called system tests, integration tests or regression tests.

- before refactoring ensure that you have a way of testing your code
- the tests should be easy to run (ideally just one command) and fast (seconds is better than minutes)
- run your tests after completing every change to ensure that you haven't broken anything
- fix any errors or bugs you have introduced before moving onto the next step

Research scripts and notebooks may not be in a state where they are ready to have formal tests written for them: in this case it is often enough to have a small validation input dataset and a corresponding set of correct outputs. The key is that these should be fast to run and easy to validate, particularly if you are doing so manually.

## Refactoring Research Scripts

Often when working on new ideas you end up with a script or a notebook that does an analysis that you want, and does it correctly.  In some cases that is good enough: it works, it's replicable, and you don't need to extend it. And that's fine.

But often you find yourself needing slightly different versions of it: maybe you need it to read a different file, or output to a different format, or do an analysis on different dimensions. So you copy the script and modify it. Each time there is a change you risk breaking the entire workflow. Sometimes you find yourself going back to old versions to copy bits and pieces into your new script. Or sometimes you want to share your work and expand it's impact. It's unlikely that your script written exactly as-is will do what every potential user needs. If you can provide a library of useful code alongside the script, others will be able to use, re-use and adapt your code for their tasks.

In these cases it's worth pausing and spending a few hours or a day *refactoring* your code: restructuring the code without significantly changing its external behaviour.

Refactoring research code often goes through a number of steps:
- create a main function and add tests
- turn code blocks into a library of *functions*
- *parametrise* the functions
- turn groups of functions into *classes*
- split the code into *modules*

This is an incremental process, and at the end of each step you will have working code, validated by tests, which is easier to test and easier to modify in the future, so you can always stop at the point which feels right for your use case.
