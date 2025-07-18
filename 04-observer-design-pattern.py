from abc import ABC, abstractmethod
# There is a observable and observers
# Wherever there is a state change in observable the it should notify all observers

# E.g - Wheather Station has a task to change temperature constantly and 
# a lot ob observers on it like news, websites, tv, mobile


class Observable(ABC):
    # observerList = [] We can't initialize in interface
    @abstractmethod
    def add(self):
        pass

    @abstractmethod
    def remove(self):
        pass

    @abstractmethod
    def notify(self):
        pass


class Observer(ABC):

    @abstractmethod
    def update(delf):
        pass

class WheatherStationObservable(Observable):
    observers = []
    current_temperature = None
    def add(self, observer: Observer):
        self.observers.append(observer)
    
    def remove(self, observer: Observer):
        if observer in self.observers:
            self.observers.remove(observer)
    
    def notify(self):
        for observer in self.observers:
            observer.update(self.current_temperature)

    def setData(self, new_temperature):
        self.current_temperature = new_temperature
        self.notify()

class MobileObserver(Observer):
    def update(self, current_temperature):
        print(f"This is a mobile and the current temperature is: {current_temperature}")

class TVObserver(Observer):
    def update(self, current_temperature):
        print(f"This is a t.v. and the current temperature is: {current_temperature}")


mobile1 = MobileObserver()
mobile2 = MobileObserver()
tv1 = TVObserver()
tv2 = TVObserver()

wso = WheatherStationObservable()
wso.add(mobile1)
wso.add(mobile2)
wso.add(tv1)
wso.add(tv2)

wso.setData(10)
print("-----------------------------------------------------------")
wso.setData(20)
print("-----------------------------------------------------------")
wso.setData(30)
print("-----------------------------------------------------------")
wso.setData(40)


