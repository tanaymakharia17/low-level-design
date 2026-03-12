
# Requirements:

# - Insert coins
# - select tray code for the product


from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum
import threading


# ============================================================================
# Data Classes (DB Tables)
# ============================================================================

class Product:
    def __init__(self, id: int, name: str, price: int):
        self.id = id
        self.name = name
        self.price = price

    def __repr__(self):
        return f"Product({self.id}, {self.name}, price={self.price})"


class VendingMachineTray:
    def __init__(self, id: int, vending_machine_id: int, product_id: int, quantity: int, tray_code: str):
        self.id = id
        self.vending_machine_id = vending_machine_id
        self.product_id = product_id
        self.quantity = quantity
        self.tray_code = tray_code


class VendingMachineStateTable:
    def __init__(self, id: int, vending_machine_id: int, state: str, inserted_amount: int, selected_product_id: int | None):
        self.id = id
        self.vending_machine_id = vending_machine_id
        self.state = state
        self.inserted_amount = inserted_amount
        self.selected_product_id = selected_product_id


class VendingMachineTable:
    def __init__(self, id: int, name: str, location: str):
        self.id = id
        self.name = name
        self.location = location


class Coin(Enum):
    PENNY = 1
    NICKEL = 5
    DIME = 10
    QUARTER = 25
    DOLLAR = 100


# ============================================================================
# Repositories
# ============================================================================

class ProductRepository:
    def __init__(self):
        self._products: dict[int, Product] = {}

    def add(self, product: Product):
        self._products[product.id] = product

    def get_by_id(self, product_id: int) -> Product | None:
        return self._products.get(product_id)


class VendingMachineTrayRepository:
    def __init__(self):
        self._trays: list[VendingMachineTray] = []

    def add(self, tray: VendingMachineTray):
        self._trays.append(tray)

    def get_by_code_and_machine(self, tray_code: str, vending_machine_id: int) -> VendingMachineTray | None:
        for tray in self._trays:
            if tray.tray_code == tray_code and tray.vending_machine_id == vending_machine_id:
                return tray
        return None

    def reduce_stock(self, tray: VendingMachineTray):
        if tray.quantity <= 0:
            raise ValueError(f"Tray {tray.tray_code} is out of stock")
        tray.quantity -= 1


class VendingMachineRepository:
    def __init__(self):
        self._machines: dict[int, VendingMachineTable] = {}

    def add(self, machine: VendingMachineTable):
        self._machines[machine.id] = machine

    def get_by_id(self, machine_id: int) -> VendingMachineTable | None:
        return self._machines.get(machine_id)


# ============================================================================
# State Pattern
# ============================================================================

class VendingMachineState(ABC):
    @abstractmethod
    def insert_coin(self, coin: Coin, machine: VendingMachine) -> None:
        pass

    @abstractmethod
    def select_product(self, tray_code: str, machine: VendingMachine) -> None:
        pass

    @abstractmethod
    def dispense(self, machine: VendingMachine) -> None:
        pass

    @abstractmethod
    def cancel(self, machine: VendingMachine) -> None:
        pass


class IdleState(VendingMachineState):
    def insert_coin(self, coin: Coin, machine: VendingMachine):
        machine.balance += coin.value
        machine.set_state(machine.has_money_state)
        print(f"  Inserted {coin.name} ({coin.value}). Balance: {machine.balance}")

    def select_product(self, tray_code: str, machine: VendingMachine):
        raise Exception("Insert coins first")

    def dispense(self, machine: VendingMachine):
        raise Exception("Insert coins and select a product first")

    def cancel(self, machine: VendingMachine):
        raise Exception("No transaction in progress")


class HasMoneyState(VendingMachineState):
    def insert_coin(self, coin: Coin, machine: VendingMachine):
        machine.balance += coin.value
        print(f"  Inserted {coin.name} ({coin.value}). Balance: {machine.balance}")

    def select_product(self, tray_code: str, machine: VendingMachine):
        tray = machine.tray_repo.get_by_code_and_machine(tray_code, machine.machine_id)
        if tray is None:
            raise Exception(f"No tray found for code {tray_code}")
        if tray.quantity <= 0:
            raise Exception(f"Product at tray {tray_code} is out of stock")

        product = machine.product_repo.get_by_id(tray.product_id)
        if product is None:
            raise Exception(f"Product not found for tray {tray_code}")
        if machine.balance < product.price:
            raise Exception(
                f"Insufficient balance. Need {product.price}, have {machine.balance}. "
                f"Insert {product.price - machine.balance} more."
            )

        machine.selected_tray_code = tray_code
        machine.set_state(machine.dispensing_state)
        print(f"  Selected {product.name} at {tray_code} (price: {product.price})")

    def dispense(self, machine: VendingMachine):
        raise Exception("Select a product first")

    def cancel(self, machine: VendingMachine):
        refund = machine.balance
        machine.balance = 0
        machine.set_state(machine.idle_state)
        print(f"  Transaction cancelled. Refunded: {refund}")


class DispensingState(VendingMachineState):
    def insert_coin(self, coin: Coin, machine: VendingMachine):
        raise Exception("Cannot insert coins while dispensing")

    def select_product(self, tray_code: str, machine: VendingMachine):
        raise Exception("Cannot select product while dispensing")

    def dispense(self, machine: VendingMachine):
        tray = machine.tray_repo.get_by_code_and_machine(machine.selected_tray_code, machine.machine_id)
        product = machine.product_repo.get_by_id(tray.product_id)

        machine.tray_repo.reduce_stock(tray)
        change = machine.balance - product.price
        machine.balance = 0
        machine.selected_tray_code = None
        machine.set_state(machine.idle_state)

        print(f"  Dispensed: {product.name}. Change returned: {change}")

    def cancel(self, machine: VendingMachine):
        refund = machine.balance
        machine.balance = 0
        machine.selected_tray_code = None
        machine.set_state(machine.idle_state)
        print(f"  Transaction cancelled. Refunded: {refund}")


# ============================================================================
# VendingMachine (Context)
# ============================================================================

class VendingMachine:
    def __init__(self, machine_id: int, product_repo: ProductRepository, tray_repo: VendingMachineTrayRepository):
        self.machine_id = machine_id
        self.product_repo = product_repo
        self.tray_repo = tray_repo
        self.balance = 0
        self.selected_tray_code: str | None = None
        self._lock = threading.Lock()

        self.idle_state = IdleState()
        self.has_money_state = HasMoneyState()
        self.dispensing_state = DispensingState()

        self._current_state: VendingMachineState = self.idle_state

    def set_state(self, state: VendingMachineState):
        self._current_state = state

    def insert_coin(self, coin: Coin):
        with self._lock:
            self._current_state.insert_coin(coin, self)

    def select_product(self, tray_code: str):
        with self._lock:
            self._current_state.select_product(tray_code, self)

    def dispense(self):
        with self._lock:
            self._current_state.dispense(self)

    def cancel(self):
        with self._lock:
            self._current_state.cancel(self)


# ============================================================================
# Controller
# ============================================================================

class VendingMachineController:

    def __init__(self, machine_repo: VendingMachineRepository,
                 product_repo: ProductRepository, tray_repo: VendingMachineTrayRepository):
        self.machine_repo = machine_repo
        self.product_repo = product_repo
        self.tray_repo = tray_repo
        self._machines: dict[int, VendingMachine] = {}

    def _get_machine(self, machine_id: int) -> VendingMachine:
        if machine_id not in self._machines:
            machine_table = self.machine_repo.get_by_id(machine_id)
            if machine_table is None:
                raise Exception(f"Vending machine {machine_id} not found")
            self._machines[machine_id] = VendingMachine(machine_id, self.product_repo, self.tray_repo)
        return self._machines[machine_id]

    def insert_coin(self, machine_id: int, coin: Coin):
        self._get_machine(machine_id).insert_coin(coin)

    def select_product(self, machine_id: int, tray_code: str):
        self._get_machine(machine_id).select_product(tray_code)

    def dispense(self, machine_id: int):
        self._get_machine(machine_id).dispense()

    def cancel(self, machine_id: int):
        self._get_machine(machine_id).cancel()


# ============================================================================
# Demo
# ============================================================================

if __name__ == "__main__":
    # Setup repositories
    product_repo = ProductRepository()
    product_repo.add(Product(1, "Coke", 150))
    product_repo.add(Product(2, "Water", 100))
    product_repo.add(Product(3, "Chips", 200))

    tray_repo = VendingMachineTrayRepository()
    tray_repo.add(VendingMachineTray(1, 1, 1, 5, "A1"))   # Coke, qty 5
    tray_repo.add(VendingMachineTray(2, 1, 2, 3, "A2"))   # Water, qty 3
    tray_repo.add(VendingMachineTray(3, 1, 3, 0, "B1"))   # Chips, qty 0 (out of stock)

    machine_repo = VendingMachineRepository()
    machine_repo.add(VendingMachineTable(1, "Lobby Machine", "Building A Lobby"))

    controller = VendingMachineController(machine_repo, product_repo, tray_repo)

    MID = 1  # machine_id passed in each API call

    # --- Happy path: buy a Coke (price 150) ---
    print("\n--- Happy Path: Buy Coke ---")
    controller.insert_coin(MID, Coin.DOLLAR)
    controller.insert_coin(MID, Coin.QUARTER)
    controller.insert_coin(MID, Coin.QUARTER)
    controller.select_product(MID, "A1")
    controller.dispense(MID)

    # --- Edge case: insufficient balance ---
    print("\n--- Edge Case: Insufficient Balance ---")
    controller.insert_coin(MID, Coin.QUARTER)
    try:
        controller.select_product(MID, "A1")
    except Exception as e:
        print(f"  Error (expected): {e}")
    controller.insert_coin(MID, Coin.DOLLAR)
    controller.insert_coin(MID, Coin.QUARTER)
    controller.select_product(MID, "A1")
    controller.dispense(MID)

    # --- Edge case: out of stock ---
    print("\n--- Edge Case: Out of Stock ---")
    controller.insert_coin(MID, Coin.DOLLAR)
    controller.insert_coin(MID, Coin.DOLLAR)
    try:
        controller.select_product(MID, "B1")
    except Exception as e:
        print(f"  Error (expected): {e}")
    controller.cancel(MID)

    # --- Edge case: invalid tray code ---
    print("\n--- Edge Case: Invalid Tray Code ---")
    controller.insert_coin(MID, Coin.DOLLAR)
    try:
        controller.select_product(MID, "Z9")
    except Exception as e:
        print(f"  Error (expected): {e}")
    controller.cancel(MID)

    # --- Edge case: cancel mid-transaction ---
    print("\n--- Edge Case: Cancel Transaction ---")
    controller.insert_coin(MID, Coin.DOLLAR)
    controller.insert_coin(MID, Coin.DOLLAR)
    controller.cancel(MID)

    # --- Edge case: wrong state actions ---
    print("\n--- Edge Case: Wrong State Actions ---")
    try:
        controller.select_product(MID, "A1")
    except Exception as e:
        print(f"  Error (expected): {e}")
    try:
        controller.dispense(MID)
    except Exception as e:
        print(f"  Error (expected): {e}")
