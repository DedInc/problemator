<h1 align="center">problemator - WolframAlpha's Unlimited AI-generated practice problems and answers API wrapper.</h1>

<br>

<h1 align="center"> -How to use- </h1>

```python
from problemator import *
from random import choice

loadSession()  # Initialize
print(getCategories())  # See categories

category = getCategory(0)  # Get Addition

# LVL: 0 - Beginner; 1 - Intermediate; 2 - Advanced
# Count - Number of problems
# type - Category
problem = generateProblem(lvl=0, type=category) # Generate a problem

print(problem['text'])  # Text of the problem
print(problem['image'])  # Image of the problem
print(problem['difficulty'])  # Difficulty of the problem

c = checkProblem(problem, 'x+5')  # Check problem, where x+5 - answer
print(c['correct'])  # True or False
print(c['hint'])  # Image of the Hint
print(c['solution'])  # Image of the Solution
```