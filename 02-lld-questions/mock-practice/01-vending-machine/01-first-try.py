# Requirements:

# - Insert coins
# - select tray code for the product
# - one product at a time
# - changes should be returned
# - if product not available return money
# - if product is available, dispense the product



# # Approach:
# - Use state design pattern for the current state of the vending machine


# classes:
# - Abstract VendingMachineState
#     - insertCoin(coins: list[int])
#     - selectProduct(product: str)
#     - dispense()
#     - returnChange()
# - IdleState (VendingMachineState)
# - HasMoneyState (VendingMachineState)
# - DispensingProductState (VendingMachineState)
# - ReturningChangeState (VendingMachineState)

# - VendingMachineService
#     - insertCoin(coins: list[int])
#     - selectProduct(product: str)
#     - dispense()
#     - returnChange()

# - VendingMachineController
#     - insertCoin(coins: list[int])
#     - selectProduct(product: str)
#     - dispense()
#     - returnChange()


# - ProductStock: # this is db object
#     - id: int
#     - name: str
#     - quantity: int
#     - price: int
#     - trayCode: str

# - ProductStockRepository:
#     - products: list[ProductStock]
#     - getProductStock(id: int) -> ProductStock
#     - reduceProductStockByOne(id: int)



# Implementation:

from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum



class SuccessOrFailure(Enum):
    SUCCESS = "success"
    FAILURE = "failure"


class ProductStock:
    def __init__(self, id: int, name: str, quantity: int, price: int, trayCode: str):
        self.id = id
        self.name = name
        self.quantity = quantity
        self.price = price
        self.trayCode = trayCode

class ProductStockRepository:
    def __init__(self):
        self.products = []
    
    def getProductStock(self, product_id: int) -> ProductStock:
        for product in self.products:
            if product.id == product_id:
                return product
        return None
    
    def addProductStock(self, product_stock: ProductStock):
        self.products.append(product_stock)
    
    def updateProductStock(self, product_id: int, product_stock: ProductStock):
        for product in self.products:
            if product.id == product_id:
                product.quantity = product_stock.quantity
                return




class AbstractVendingMachineState(ABC):

    total_money_inserted: int
    selected_product_id: int
    product_stock_repository: ProductStockRepository

    @abstractmethod
    def insertCoin(self, amount: int, vending_machine_service: VendingMachineService) -> SuccessOrFailure: 
        pass

    @abstractmethod
    def selectProduct(self, product_id: int, vending_machine_service: VendingMachineService) -> SuccessOrFailure:
        pass

    @abstractmethod
    def dispense(self, vending_machine_service: VendingMachineService) -> SuccessOrFailure:
        pass

    @abstractmethod
    def returnChange(self, vending_machine_service: VendingMachineService) -> SuccessOrFailure:
        pass


class IdleState(AbstractVendingMachineState):

    def insertCoin(self, amount: int, vending_machine_service: VendingMachineService) -> SuccessOrFailure:
        if amount <= 0:
            return SuccessOrFailure.FAILURE
        vending_machine_service.inserted_amount += amount
        vending_machine_service.currentState = vending_machine_service.has_money_state
        print(f"Inserted {amount} coins. Total amount: {vending_machine_service.inserted_amount}")
        return SuccessOrFailure.SUCCESS
    
    def selectProduct(self, product: str, vending_machine_service: VendingMachineService) -> SuccessOrFailure:
        return SuccessOrFailure.FAILURE
    
    def dispense(self, vending_machine_service: VendingMachineService) -> SuccessOrFailure:
        return SuccessOrFailure.FAILURE

    def returnChange(self, vending_machine_service: VendingMachineService) -> SuccessOrFailure:
        return SuccessOrFailure.FAILURE


class HasMoneyState(AbstractVendingMachineState):
    def insertCoin(self, amount: int, vending_machine_service: VendingMachineService) -> SuccessOrFailure:
        if amount <= 0:
            return SuccessOrFailure.FAILURE
        vending_machine_service.inserted_amount += amount
        print(f"Inserted {amount} coins. Total amount: {vending_machine_service.inserted_amount}")
        return SuccessOrFailure.SUCCESS
    
    def selectProduct(self, product_id: int, vending_machine_service: VendingMachineService) -> SuccessOrFailure:
        product_stock = vending_machine_service.productStockRepository.getProductStock(product_id)
        if product_stock is None or product_stock.quantity <= 0:
            return SuccessOrFailure.FAILURE

        vending_machine_service.selected_product_id = product_id
        vending_machine_service.currentState = vending_machine_service.dispensing_product_state
        print(f"Selected product {product_id}. Total amount: {vending_machine_service.inserted_amount}")

        return SuccessOrFailure.SUCCESS
    
    def dispense(self, vending_machine_service: VendingMachineService) -> SuccessOrFailure:
        return SuccessOrFailure.FAILURE
    
    def returnChange(self, vending_machine_service: VendingMachineService) -> SuccessOrFailure:
        change = vending_machine_service.inserted_amount
        vending_machine_service.inserted_amount = 0
        vending_machine_service.currentState = vending_machine_service.returning_change_state
        print(f"Returning change: {change}")
        return SuccessOrFailure.SUCCESS

class DispensingProductState(AbstractVendingMachineState):
    def insertCoin(self, amount: int, vending_machine_service: VendingMachineService) -> SuccessOrFailure:
        return SuccessOrFailure.FAILURE
    
    def selectProduct(self, product_id: int, vending_machine_service: VendingMachineService) -> SuccessOrFailure:
        return SuccessOrFailure.FAILURE
    
    def dispense(self, vending_machine_service: VendingMachineService) -> SuccessOrFailure:
        product_stock = vending_machine_service.productStockRepository.getProductStock(vending_machine_service.selected_product_id)
        if product_stock is None or product_stock.quantity <= 0:
            vending_machine_service.currentState = vending_machine_service.selecting_product_state
            return SuccessOrFailure.FAILURE
        
        change = vending_machine_service.inserted_amount - product_stock.price
        if change < 0:
            vending_machine_service.currentState = vending_machine_service.has_money_state
            return SuccessOrFailure.FAILURE
        product_stock.quantity -= 1
        vending_machine_service.productStockRepository.updateProductStock(vending_machine_service.selected_product_id, product_stock)
        vending_machine_service.currentState = vending_machine_service.returning_change_state
        print(f"Dispensed product {vending_machine_service.selected_product_id}. Change: {change}")
        return SuccessOrFailure.SUCCESS
    
    def returnChange(self, vending_machine_service: VendingMachineService) -> SuccessOrFailure:
        change = vending_machine_service.inserted_amount
        vending_machine_service.inserted_amount = 0
        vending_machine_service.currentState = vending_machine_service.idle_state
        print(f"Returning change: {change}")
        return SuccessOrFailure.SUCCESS

class ReturningChangeState(AbstractVendingMachineState):
    def insertCoin(self, amount: int, vending_machine_service: VendingMachineService) -> SuccessOrFailure:
        return SuccessOrFailure.FAILURE
    
    def selectProduct(self, product_id: int, vending_machine_service: VendingMachineService) -> SuccessOrFailure:
        return SuccessOrFailure.FAILURE
    
    def dispense(self, vending_machine_service: VendingMachineService) -> SuccessOrFailure:
        return SuccessOrFailure.FAILURE
    
    def returnChange(self, vending_machine_service: VendingMachineService) -> SuccessOrFailure:
        change = vending_machine_service.inserted_amount
        vending_machine_service.inserted_amount = 0
        vending_machine_service.currentState = vending_machine_service.idle_state
        print(f"Returning change: {change}")
        return SuccessOrFailure.SUCCESS

class VendingMachineService:

    def __init__(self, productStockRepository: ProductStockRepository):
        self.productStockRepository = productStockRepository

        self.idle_state = IdleState()
        self.has_money_state = HasMoneyState()
        self.dispensing_product_state = DispensingProductState()
        self.returning_change_state = ReturningChangeState()

        self.currentState = IdleState()

        self.inserted_amount = 0
        self.selected_product_id = None

    
    def insertCoin(self, coins: list[int]) -> SuccessOrFailure:
        return self.currentState.insertCoin(coins, self)
    
    def selectProduct(self, product: str) -> SuccessOrFailure:
        return self.currentState.selectProduct(product, self)
    
    def dispense(self) -> SuccessOrFailure:
        return self.currentState.dispense(self)
    
    def returnChange(self) -> SuccessOrFailure:
        return self.currentState.returnChange(self)



class VendingMachineController:
    def __init__(self, vending_machine_service: VendingMachineService):
        self.vending_machine_service = vending_machine_service

    def insertCoin(self, coins: list[int]) -> SuccessOrFailure:
        return self.vending_machine_service.insertCoin(coins)
    
    def selectProduct(self, product: str) -> SuccessOrFailure:
        return self.vending_machine_service.selectProduct(product)
    
    def dispense(self) -> SuccessOrFailure:
        return self.vending_machine_service.dispense()
    
    def returnChange(self) -> SuccessOrFailure:
        return self.vending_machine_service.returnChange()





if __name__ == "__main__":
    product_stock_repository = ProductStockRepository()
    product_stock_repository.addProductStock(ProductStock(1, "Coke", 10, 100, "A1"))
    product_stock_repository.addProductStock(ProductStock(2, "Pepsi", 10, 100, "A2"))
    product_stock_repository.addProductStock(ProductStock(3, "Soda", 10, 100, "A3"))
    product_stock_repository.addProductStock(ProductStock(4, "Water", 10, 100, "A4"))
    product_stock_repository.addProductStock(ProductStock(5, "Juice", 10, 100, "A5"))
    product_stock_repository.addProductStock(ProductStock(6, "Tea", 10, 100, "A6"))
    product_stock_repository.addProductStock(ProductStock(7, "Coffee", 10, 100, "A7"))

    vending_machine_service = VendingMachineService(product_stock_repository)
    vending_machine_controller = VendingMachineController(vending_machine_service)

    vending_machine_controller.insertCoin(100)
    vending_machine_controller.selectProduct(1)
    vending_machine_controller.dispense()
    vending_machine_controller.returnChange()

    # invalid states
    vending_machine_controller.insertCoin(-1)
    vending_machine_controller.selectProduct(1)
    vending_machine_controller.dispense()
    vending_machine_controller.returnChange()
    vending_machine_controller.insertCoin(100)
    vending_machine_controller.selectProduct(1)
    vending_machine_controller.dispense()
    vending_machine_controller.returnChange()
    vending_machine_controller.insertCoin(100)
    vending_machine_controller.selectProduct(1)
    vending_machine_controller.dispense()
    vending_machine_controller.returnChange()


