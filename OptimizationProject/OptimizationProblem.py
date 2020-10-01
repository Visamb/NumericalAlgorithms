#Its constructor should take an
#objective function as input, optionally also its gradient can be provided.

class Optimize:

    def __init__(self, function, gradient):
        self.function = function
        self.gradient = gradient


    def __call__(self):
        """Optimize function and return optimal input value?"""




