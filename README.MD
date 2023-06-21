<h1 align="center">problemator - WolframAlpha's Unlimited AI-generated practice problems and answers API wrapper.</h1>

<br>

<h1 align="center"> -How to use- </h1>

```python
from problemator import Problemator
from random import choice

p = Problemator()  # Initialize
print(p.categories)  # See categories

category = p.get_category(0)  # Get Addition

# LVL: 0 - Beginner; 1 - Intermediate; 2 - Advanced
# Count - Number of problems
# type - Category
problem = p.generate_problem(lvl=0, type=category) # Generate a problem

print(problem['text'])  # Text of the problem
print(problem['image'])  # Image of the problem
print(problem['difficulty'])  # Difficulty of the problem

result = p.check_problem(problem, 'x+5')  # Check problem, where x+5 - answer
print(result['correct'])  # True or False
print(result['attempt'])  # Image of the Attempt
print(result['hint'])  # Image of the Hint
print(result['solution'])  # Image of the Solution
```