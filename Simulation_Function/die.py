from random import randint, choices

class Die:
    """A class representing a single die."""
    
    def __init__(self, num_sides=6):
        """Assume a six-sided die."""
        self.num_sides = num_sides
        
    def roll(self):
        """Return a random value based on probabilities."""
        if self.num_sides == 6:
            return randint(1, self.num_sides)
        else:  
            return choices(range(1, self.num_sides + 3))[0]
