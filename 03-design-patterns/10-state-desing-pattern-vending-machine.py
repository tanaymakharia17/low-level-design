from abc import ABC, abstractmethod


class State(ABC):
    @abstractmethod
    def insert_coin(self, machine, amount): pass
    @abstractmethod
    def select_product(self, machine, product): pass
    @abstractmethod
    def dispense(self, machine): pass

class IdleState(State):
    def insert_coin(self, machine, amount):
        machine.balance += amount
        machine.set_state(machine.has_money_state)
    def select_product(self, machine, product):
        print("Insert money first.")
    def dispense(self, machine):
        print("Insert money first.")


class HasMoneyState(State):
    def insert_coin(self, machine, amount):
        machine.balance += amount
    def select_product(self, machine, product):
        if machine.inventory.get(product, 0) <= 0:
            machine.set_state(machine.out_of_stock_state)
        elif machine.balance >= machine.prices.get(product, 0):
            machine.selected_product = product
            machine.set_state(machine.dispensing_state)
        else:
            print("Insufficient balance.")
    def dispense(self, machine):
        print("Select a product first.")

    
class DispensingState(State):
    def insert_coin(self, machine, amount):
        print("Wait for the current transaction.")
    def select_product(self, machine, product):
        print("Product is being dispensed.")
    def dispense(self, machine):
        price = machine.prices.get(machine.selected_product, 0)
        machine.inventory[machine.selected_product] -= 1
        machine.balance -= price
        print(f"Dispensing {machine.selected_product}. Change ${machine.balance}")
        machine.set_state(machine.idle_state)


class OutOfStockState(State):
    def insert_coin(self, machine, amount):
        print("Machine is out of stock.")
    def select_product(self, machine, product):
        print("Machine is out of stock.")
    def dispense(self, machine):
        print("Machine is out of stock.")

class VendingMachine:
    def __init__(self, inventory, prices):
        self.inventory = inventory
        self.prices = prices
        self.balance = 0
        self.selected_product = None
        self.idle_state = IdleState()
        self.has_money_state = HasMoneyState()
        self.dispensing_state = DispensingState()
        self.out_of_stock_state = OutOfStockState()
        self.state = self.idle_state
    def set_state(self, state): self.state = state
    def insert_coin(self, amount): 
        self.state.insert_coin(self, amount)
        
    def select_product(self, product): self.state.select_product(self, product)
    def dispense(self): self.state.dispense(self)

# Main test
if __name__ == "__main__":
    inventory = {'coke': 2, 'pepsi': 1}
    prices = {'coke': 1.5, 'pepsi': 2.0}
    machine = VendingMachine(inventory, prices)
    machine.insert_coin(2.0)
    machine.select_product("coke")
    machine.dispense()
    machine.insert_coin(1.0)
    machine.select_product("pepsi")
    machine.dispense()
    machine.select_product("coke")

    # arr = [0] * 10
    # for i in range(len(arr)):
    #     arr[i] += 1 
    #     if i != 0:
    #         arr[i] += arr[i-1]
    # print(arr)