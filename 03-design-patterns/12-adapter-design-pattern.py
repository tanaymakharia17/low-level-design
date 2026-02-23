"""
Power adapter pattern
i have dubai apple laptop charger wire and in india i have other type of sockewt.
Now i used a new plug+socket to make this work from amazon

I want jason -> adapler changes xml to jsom <- Can only send xml
"""


from abc import ABC, abstractmethod


class WeightMachine(ABC):
    @abstractmethod
    def getWeightInPounds(self): pass

class BabyWeightMachine(WeightMachine):

    def getWeightInPounds(self):
        return 28
    

# Now i want weight in kg then i do is adapter

class WeightMachineAdapter(ABC):
    @abstractmethod
    def getWeightInKg(self): pass

# concrete adapter
class WeightMachineAdapterImpl(WeightMachineAdapter):
    weightMachine: WeightMachine = None

    def __init__(self, weightMachine: WeightMachine):
        self.weightMachine = weightMachine

    def getWeightInKg(self):
        return self.weightMachine.getWeightInPounds() * 0.45
    



poundMachine = BabyWeightMachine()
print(poundMachine.getWeightInPounds())

kgMachine = WeightMachineAdapterImpl(poundMachine)

print(kgMachine.getWeightInKg())