from abc import ABC, abstractmethod

# Suppose we a base car, now we want to add different features to it like, A.C., power stering, heater, power window.
# Now instead of creating new class again of multiple different combinations use decorator pattern


class BasePizza(ABC):

    @abstractmethod
    def cost(self):
        pass


class Margherita(BasePizza):

    def cost(self):
        print("Selected base pizza is margherita.")
        return 100
    
class VeggiDelight(BasePizza):

    def cost(self):
        print("Selected base pizza is veggi delight.")
        return 140
    
class PizzaDecorator(ABC):
    # base pizza = 
    @abstractmethod
    def cost(self):
        pass

class ExtraCheese(PizzaDecorator):
    def __init__(self, pizza):
        self._pizza = pizza
    
    def cost(self):
        
        cost = self._pizza.cost() + 50
        print("Added extra cheese.")
        return cost

class ExtraCorn(PizzaDecorator):
    def __init__(self, pizza):
        self._pizza = pizza
    
    def cost(self):
        
        cost = self._pizza.cost() + 30
        print("Added extra corn.")
        return cost


base_pizza = Margherita()
added_cheese = ExtraCheese(base_pizza)
added_corn = ExtraCorn(added_cheese)
print(added_corn.cost())