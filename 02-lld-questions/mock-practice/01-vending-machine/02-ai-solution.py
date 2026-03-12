
# ============================================================================
# ANSWER — CLEAN IMPLEMENTATION + INTERVIEW FLOW
# ============================================================================

# ============================================================================
# INTERVIEW FLOW (45-60 min round)
# ============================================================================

# PHASE 1: Requirements Gathering (3-5 min)
# ------------------------------------------
# Ask these clarifying questions OUT LOUD before writing anything:
#
# 1. "Can the user insert multiple coins one by one, or all at once?"
#    -> Usually one by one, accept specific denominations (1, 5, 10, 25)
# 2. "How does the user select a product — by tray code like A1, B2?"
#    -> Yes, tray code, not product ID
# 3. "Should the machine handle multiple purchases in sequence?"
#    -> Yes, after one transaction completes, machine goes back to idle
# 4. "Do we need to handle concurrent users?"
#    -> Mention it, implement a lock, but don't over-engineer
# 5. "Should we support admin operations like restocking?"
#    -> Ask, but usually out of scope for the interview
#
# Write down the confirmed requirements before moving on.


# PHASE 2: Identify Entities + Pattern (3-5 min)
# -----------------------------------------------
# Say out loud:
# "This problem has clear states — idle, has money, dispensing.
#  Each state allows only certain actions.
#  I'll use the STATE DESIGN PATTERN."
#
# Then sketch the state transitions:
#
#   IDLE --insertCoin--> HAS_MONEY
#   HAS_MONEY --insertCoin--> HAS_MONEY (add more)
#   HAS_MONEY --selectProduct--> DISPENSING (if valid product + enough money)
#   HAS_MONEY --cancel--> IDLE (return all money)
#   DISPENSING --dispense--> IDLE (dispense product + return change atomically)
#
# Key insight: dispensing + change return should be ONE atomic operation,
# not two separate states. This simplifies the design.


# PHASE 3: Class Design (5 min)
# ------------------------------
# List classes and their responsibilities on the whiteboard/doc:
#
# - Product (data class: name, price, tray_code)
# - Inventory (manages stock by tray_code, thread-safe)
# - Coin enum (valid denominations)
# - VendingMachineState (ABC with insert_coin, select_product, dispense, cancel)
# - IdleState, HasMoneyState, DispensingState (concrete states)
# - VendingMachine (context object, holds current state + balance)
#
# SAY: "I'm keeping it to these classes to stay focused.
#       I'll skip the controller layer since it would be a pure pass-through."


# PHASE 4: Implementation (25-30 min)
# ------------------------------------
# Code in this order:
#   1. Data classes (Product, Coin, Inventory) — 5 min
#   2. State ABC — 2 min
#   3. VendingMachine (context) — 5 min
#   4. Each concrete state — 10 min
#   5. Demo in main — 5 min

import threading


class Coin(Enum):
    PENNY = 1
    NICKEL = 5
    DIME = 10
    QUARTER = 25
    DOLLAR = 100


class Product:
    def __init__(self, name: str, price: int, tray_code: str):
        self.name = name
        self.price = price
        self.tray_code = tray_code

    def __repr__(self):
        return f"Product({self.name}, price={self.price}, tray={self.tray_code})"


class Inventory:
    def __init__(self):
        self._stock: dict[str, tuple[Product, int]] = {}  # tray_code -> (product, qty)
        self._lock = threading.Lock()

    def add_product(self, product: Product, quantity: int):
        with self._lock:
            self._stock[product.tray_code] = (product, quantity)

    def get_product(self, tray_code: str) -> Product | None:
        entry = self._stock.get(tray_code)
        return entry[0] if entry else None

    def is_available(self, tray_code: str) -> bool:
        entry = self._stock.get(tray_code)
        return entry is not None and entry[1] > 0

    def reduce_stock(self, tray_code: str):
        with self._lock:
            product, qty = self._stock[tray_code]
            if qty <= 0:
                raise ValueError(f"Product at {tray_code} is out of stock")
            self._stock[tray_code] = (product, qty - 1)


class VendingMachineState2(ABC):
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


class IdleState2(VendingMachineState2):
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


class HasMoneyState2(VendingMachineState2):
    def insert_coin(self, coin: Coin, machine: VendingMachine):
        machine.balance += coin.value
        print(f"  Inserted {coin.name} ({coin.value}). Balance: {machine.balance}")

    def select_product(self, tray_code: str, machine: VendingMachine):
        product = machine.inventory.get_product(tray_code)
        if product is None:
            raise Exception(f"No product at tray {tray_code}")
        if not machine.inventory.is_available(tray_code):
            raise Exception(f"{product.name} is out of stock")
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


class DispensingState2(VendingMachineState2):
    def insert_coin(self, coin: Coin, machine: VendingMachine):
        raise Exception("Cannot insert coins while dispensing")

    def select_product(self, tray_code: str, machine: VendingMachine):
        raise Exception("Cannot select product while dispensing")

    def dispense(self, machine: VendingMachine):
        product = machine.inventory.get_product(machine.selected_tray_code)

        # Atomic: reduce stock, calculate change, reset machine
        machine.inventory.reduce_stock(machine.selected_tray_code)
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


class VendingMachine:
    def __init__(self, inventory: Inventory):
        self.inventory = inventory
        self.balance = 0
        self.selected_tray_code: str | None = None
        self._lock = threading.Lock()

        # Pre-create state singletons
        self.idle_state = IdleState2()
        self.has_money_state = HasMoneyState2()
        self.dispensing_state = DispensingState2()

        self._current_state: VendingMachineState2 = self.idle_state  # use the singleton

    def set_state(self, state: VendingMachineState2):
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


# PHASE 5: Demo (5 min)
# ----------------------
# Walk through happy path AND edge cases. Print expected output.

def run_answer():
    print("=" * 60)
    print("CLEAN IMPLEMENTATION DEMO")
    print("=" * 60)

    inventory = Inventory()
    inventory.add_product(Product("Coke", 150, "A1"), 5)
    inventory.add_product(Product("Water", 100, "A2"), 3)
    inventory.add_product(Product("Chips", 200, "B1"), 0)  # out of stock

    vm = VendingMachine(inventory)

    # --- Happy path: buy a Coke (price 150) with 2 dollars ---
    print("\n--- Happy Path: Buy Coke ---")
    vm.insert_coin(Coin.DOLLAR)
    vm.insert_coin(Coin.QUARTER)
    vm.insert_coin(Coin.QUARTER)
    vm.select_product("A1")
    vm.dispense()
    # Expected: Dispensed Coke. Change: 50

    # --- Edge case: not enough money ---
    print("\n--- Edge Case: Insufficient Balance ---")
    vm.insert_coin(Coin.QUARTER)
    try:
        vm.select_product("A1")  # Coke costs 150, only inserted 25
    except Exception as e:
        print(f"  Error (expected): {e}")

    # --- Continue: add more money and complete ---
    vm.insert_coin(Coin.DOLLAR)
    vm.insert_coin(Coin.QUARTER)
    vm.select_product("A1")
    vm.dispense()

    # --- Edge case: out of stock ---
    print("\n--- Edge Case: Out of Stock ---")
    vm.insert_coin(Coin.DOLLAR)
    vm.insert_coin(Coin.DOLLAR)
    try:
        vm.select_product("B1")  # Chips, qty = 0
    except Exception as e:
        print(f"  Error (expected): {e}")
    vm.cancel()

    # --- Edge case: invalid tray code ---
    print("\n--- Edge Case: Invalid Tray Code ---")
    vm.insert_coin(Coin.DOLLAR)
    try:
        vm.select_product("Z9")
    except Exception as e:
        print(f"  Error (expected): {e}")
    vm.cancel()

    # --- Edge case: cancel mid-transaction ---
    print("\n--- Edge Case: Cancel Transaction ---")
    vm.insert_coin(Coin.DOLLAR)
    vm.insert_coin(Coin.DOLLAR)
    vm.cancel()
    # Expected: Refunded 200

    # --- Edge case: wrong action in wrong state ---
    print("\n--- Edge Case: Wrong State Actions ---")
    try:
        vm.select_product("A1")  # no money inserted
    except Exception as e:
        print(f"  Error (expected): {e}")

    try:
        vm.dispense()  # nothing selected
    except Exception as e:
        print(f"  Error (expected): {e}")


# PHASE 6: Discussion Points (5 min)
# -----------------------------------
# Be READY for these follow-up questions from the interviewer:
#
# Q: "How would you handle concurrency?"
# A: Already have threading.Lock on VendingMachine. Each public method
#    acquires the lock so state transitions are atomic. For a distributed
#    system, we'd use optimistic locking on inventory in the DB.
#
# Q: "How would you add a new state like 'MaintenanceMode'?"
# A: Create MaintenanceState that rejects all operations with a message.
#    Add a method to VendingMachine to enter/exit maintenance. OCP satisfied —
#    no existing state classes need to change.
#
# Q: "How would you handle real coin change-making (e.g., return 75 as 3 quarters)?"
# A: Add a CoinInventory to the machine that tracks available coins.
#    Use a greedy algorithm (largest denomination first) to make change.
#    If exact change can't be made, reject the transaction.
#
# Q: "What if we want multiple vending machines?"
# A: Each VendingMachine instance is independent. Inventory could be
#    shared (with proper locking) or per-machine. Add a VendingMachineManager
#    if we need fleet-level operations.
#
# Q: "How would you test this?"
# A: Unit test each state in isolation — mock the machine context.
#    Integration test full flows (happy path, edge cases).
#    Test concurrency with multiple threads buying the last item.


# KEY DIFFERENCES FROM YOUR ATTEMPT (study these):
# -------------------------------------------------
# 1. States raise exceptions with clear messages, not silent FAILURE enums
# 2. Tray code selection (matches the requirement), not product ID
# 3. Price check at selection time, not at dispense time
# 4. Dispense + change return is ONE atomic operation, not two states
# 5. No ReturningChangeState — it's not a real state the machine sits in
# 6. Coin enum with valid denominations, not arbitrary int amounts
# 7. currentState initialized to self.idle_state (the singleton), not a new IdleState()
# 8. threading.Lock for concurrency safety
# 9. No controller layer (it was a pure pass-through adding no value)
# 10. balance is deducted in dispense(), so change is correct
# 11. cancel() is available in HasMoney and Dispensing states
# 12. Demo covers happy path + 5 edge cases with expected output


if __name__ == "__main__":
    run_answer()