<h1 align="center">problemator - WolframAlpha's Unlimited AI-generated practice problems and answers API wrapper.</h1>

<br>

<h1 align="center"> -How to use- </h1>

```python
from problemator import *
from random import choice

loadSession()  # Initialize
print(getCategories())  # See categories

category = getCategoryByID(0)  # Get Addition by ID
category = getCategoryByName('Add')  # Get Addition by Name

# LVL: 0 - Beginner; 1 - Intermediate; 2 - Advanced
# Count - Number of problems
# type - Category
problems = generateProblems(count=10, lvl=0, type=category)
problem = choice(problems)  # Get random problem

print(problem['problem']['text'])  # Text of the problem
print(problem['problem']['image'])  # Image of the problem

print(problem['hint'])  # Image of the hint
print(problem['solution'])  # Image of the solution
```