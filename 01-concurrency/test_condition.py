# import threading
# import time

# class ProducerConsumer:
#     def __init__(self):
#         self.queue = []
#         self.condition = threading.Condition()

#     def produce(self, item):
#         with self.condition:
#             self.queue.append(item)
#             print(f"Produced {item}")
#             self.condition.notify()  # Notify one waiting thread

#     def consume(self):
#         with self.condition:
#             while not self.queue:
#                 self.condition.wait()  # Wait for an item
#             item = self.queue.pop(0)
#             print(f"Consumed {item}")
#             return item

# class ProducerThread(threading.Thread):
#     def __init__(self, pc, name):
#         super().__init__()
#         self.pc = pc
#         self.name = name

#     def run(self):
#         for i in range(5):
#             self.pc.produce(i)
#             time.sleep(0.5)

# class ConsumerThread(threading.Thread):
#     def __init__(self, pc, name):
#         super().__init__()
#         self.pc = pc
#         self.name = name

#     def run(self):
#         for _ in range(5):
#             self.pc.consume()
#             time.sleep(1)

# # Usage
# if __name__ == "__main__":
#     pc = ProducerConsumer()

#     producer = ProducerThread(pc, "Producer")
#     consumer = ConsumerThread(pc, "Consumer")

#     producer.start()
#     consumer.start()

#     producer.join()
#     consumer.join()

#     print("Processing complete.")






#------------------------------------------------------------------------------------------------------------



import threading
import time



# send money from 1 to another acccount
# Bank each user will have a account
# there will be frequent tranctions for money
# return if operation is successfull or fail

"""
Flow:
user have a account.
user can put a request to send money to others account
send a message to the user of success or fail

classes:
Account
User
BankController
"""
class Account:
    
    def __init__(self, balance: int, user):
        self.balance = balance
        self.user = user

        self.lock = threading.Lock()
        # self.condition = threading.Condition(self.lock)
    
    def getBalance(self):
        return self.balance
    
    def addAmount(self, amount):
        time.sleep(1)
        self.balance += amount
        time.sleep(1)
    
    def deductAmount(self, amount):
        time.sleep(1)
        self.balance -= amount
        time.sleep(1)
    
    def get_lock(self):
        return self.lock

class User:
    _account = None

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def assignAccount(self, account):
        if self._account is not None:
            print("Account already exists for {self.name}.")
            return
        self._account = account
    
    def getAccount(self):
        return self._account
    
    def __str__(self):
        return f"{self.name}({self.age})"
    


class BankController:
    accounts = []
    users = []

    def addUser(self, user):
        self.users.append(user)
    
    def addAccount(self, account):
        self.accounts.append(account)

    
    def sendMoney(self, user_from, user_to, amount):
        sender_account = user_from.getAccount()
        receiver_account = user_to.getAccount()

        # Lock both accounts in consistent order to avoid deadlocks
        first_lock, second_lock = (
            (sender_account, receiver_account)
            if id(sender_account) < id(receiver_account)
            else (receiver_account, sender_account)
        )
        # with first_lock.get_lock():
        #     with second_lock.get_lock():
        if user_from.getAccount().getBalance() < amount:
            print(f"""{user_from} have a balance {user_from.getAccount().getBalance()} which is less than {amount} and can't transfer it to {user_to}""")
            return
        
        user_from.getAccount().deductAmount(amount)
        user_to.getAccount().addAmount(amount)

        print(f"Transfered {amount} from {user_from} to {user_to}.")
        print(f"{user_from} balance: {user_from.getAccount().getBalance()}")
        print(f"{user_to} balance: {user_to.getAccount().getBalance()}")

# Let's simulate concurrent transfers
def simulate_transfer(service, sender, receiver, amount):
    service.sendMoney(sender, receiver, amount)


user1 = User("Tanay", 25)
user2 = User("Nitin", 30)
user3 = User("Anya", 24)

account1 = Account(170, user1)
account2 = Account(120, user2)
account3 = Account(310, user3)


user1.assignAccount(account1)
user2.assignAccount(account2)
user3.assignAccount(account3)

controller = BankController()

controller.addUser(user1)
controller.addUser(user2)
controller.addUser(user3)

controller.addAccount(account1)
controller.addAccount(account2)
controller.addAccount(account3)


# controller.sendMoney(user1, user2, 100)
# controller.sendMoney(user1, user3, 100)
# controller.sendMoney(user2, user3, 220)

threads = []
for _ in range(3):
    t1 = threading.Thread(target=simulate_transfer, args=(controller, user1, user2, 10))
    t2 = threading.Thread(target=simulate_transfer, args=(controller, user1, user3, 20))
    t3 = threading.Thread(target=simulate_transfer, args=(controller, user2, user3, 40))

    threads.extend([t1, t2, t3])

for t in threads:
    t.start()

for t in threads:
    t.join()

print(user1.getAccount().getBalance())
print(user2.getAccount().getBalance())
print(user3.getAccount().getBalance())