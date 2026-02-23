"""


Requirements:
Add coins
After adding, select product
If coins are not enough, show not enough coins (after the user clicks dispense button)
If yes, and the user clicks dispense button and product is fetched. Rest coins are returned
At any time untill the dispense button is clicked with enough coins, there is a cancel button which will return coins

classes:
Abstract state class
Idlestateclass
havingcoinsstate
product selecting state
dispensing state
cancle state

vendingmachine controller


"""

class Product:
    name: str
    price: int

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        return f"{self.name} ({self.price} coins)"

from abc import ABC, abstractmethod

class AbstractState(ABC):
    
    @abstractmethod
    def addCoin(self, machine, coins: list[int]): pass

    @abstractmethod
    def selectProduct(self, machine, product): pass

    @abstractmethod
    def dispense(self, machine): pass

    @abstractmethod
    def cancel(self, machine): pass


class IdleState(AbstractState):
    
    def addCoin(self, machine, coins):
        machine.coins += sum(coins)
        machine.setState(machine.add_coins_state)
        print(f"Added coins: {coins}")

    def selectProduct(self, machine, product): print("Insert coins first.")

    def dispense(self, machine): print("Insert coins first.")

    def cancel(self, machine): print("Machine is resetted")




class AddCoinsState(AbstractState):
    
    def addCoin(self, machine, coins):
        machine.coins += sum(coins)
        print(f"Added coins: {coins}. Total Balance: {machine.coins}")

    def selectProduct(self, machine, product):
        if product.price <= machine.coins:
            machine.selected_product = product
            print(f"Selected Product is {product}.")
            machine.setState(machine.dispense_state)
        else:
            needed_coins = product.price - machine.coins
            print(f"Please add more coins. Short of {needed_coins} coins")
            # machine.setState(machine.idle_state)

    def dispense(self, machine): print("Select Product first.")

    def cancel(self, machine):
        machine.selected_product = None
        if machine.coins > 0:
            print(f"Collect your coins: {machine.coins}")
            machine.coins = 0
            
        
        print("Session reseted.")

        machine.setState(machine.idle_state)



class DispenseState(AbstractState):

    def addCoin(self, machine, coins): print("Coins already inserted. Product already selected.")

    def selectProduct(self, machine, product): print(f"Product already selected. Selected Product: {machine.selected_product}")

    def dispense(self, machine):
        print(f"{machine.selected_product} is dispensed")
        machine.coins -= machine.selected_product.price
        machine.selected_product = None
        if machine.coins > 0:
            machine.coins = 0
            print(f"Collect your coins: {machine.coins}")
        
        machine.setState(machine.idle_state)

    def cancel(self, machine):
        machine.selected_product = None
        if machine.coins > 0:
            print(f"Collect your coins: {machine.coins}")
            machine.coins = 0
            
        
        print("Session reseted.")

        machine.setState(machine.idle_state)


class VendingMachine:

    def __init__(self):
        self.coins = 0
        self.selected_product = None
        self.idle_state = IdleState()
        self.add_coins_state = AddCoinsState()
        self.dispense_state = DispenseState()
        self.state = self.idle_state

    def setState(self, state): self.state = state

    def addCoin(self, coins): self.state.addCoin(self, coins)

    def selectProduct(self, product): self.state.selectProduct(self, product)

    def dispense(self): self.state.dispense(self)

    def cancel(self): self.state.cancel(self)



if __name__ == "__main__":
    vm = VendingMachine()
    
    coke = Product("Coke", 10)
    chips = Product("Chips", 15)

    vm.addCoin([5])
    vm.addCoin([5])  # Balance = 10

    vm.selectProduct(coke)
    vm.dispense()

    vm.addCoin([10])
    vm.selectProduct(chips)
    vm.cancel()  # Refund 10