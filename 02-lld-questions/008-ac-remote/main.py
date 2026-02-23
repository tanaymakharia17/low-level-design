from abc import ABC, abstractmethod

# Command Interface
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

# Receiver
class AC:
    def turn_on(self):
        print("AC is turned ON")

    def turn_off(self):
        print("AC is turned OFF")

# Concrete Command to turn ON the AC
class ACOnCommand(Command):
    def __init__(self, ac: AC):
        self.ac = ac

    def execute(self):
        self.ac.turn_on()

# Concrete Command to turn OFF the AC
class ACOffCommand(Command):
    def __init__(self, ac: AC):
        self.ac = ac

    def execute(self):
        self.ac.turn_off()

# Invoker
class RemoteControl:
    def __init__(self):
        self.command = None

    def set_command(self, command: Command):
        self.command = command

    def press_button(self):
        if self.command:
            self.command.execute()
        else:
            print("No command set.")

# Driver Code
if __name__ == "__main__":
    # Receiver
    ac = AC()

    # Concrete Commands
    ac_on = ACOnCommand(ac)
    ac_off = ACOffCommand(ac)

    # Invoker
    remote = RemoteControl()

    # Turning ON the AC
    remote.set_command(ac_on)
    remote.press_button()

    # Turning OFF the AC
    remote.set_command(ac_off)
    remote.press_button()
