





"""

we initialize an notification generator object
we can send multiple type of notification from it
we can also send multiple type of messages in it



classes:
- NotificationGenarator
- NotficationChannel abc
- EmailNotificationChannel
- SMSNotificationChannel
- Formatter abc
- Html Formatter
- TextFormatter
- Message
"""
from abc import ABC, abstractmethod
import json

class Message:
    recipient: str
    email: str
    subject: str
    description: str

    def __init__(self, recipient, email, subject, description):
        self.recipient = recipient
        self.email = email
        self.subject = subject
        self.description = description

    def __repr__(self):
        return (f"Message(recipient='{self.recipient}', "
                f"email='{self.email}', "
                f"subject='{self.subject}', "
                f"description='{self.description}')")



class Formatter(ABC):

    @abstractmethod
    def format(self, message): pass


class JsonFormatter(Formatter):

    def format(self, message):
        formatter_message = {
            "recipient": message.recipient,
            "email": message.email,
            "description": message.description,
            "subject": message.subject
        }
        json_format = json.dumps(formatter_message)

        return json_format

class HTMLFormatter(Formatter):

    def format(self, message):
        html_message = f'<p> {message} </p>'
        return html_message


class NotificationChannel(ABC):

    def __init__(self, formatter: Formatter):
        self.formatter = formatter

    @abstractmethod
    def send(self): pass


class EmailNotificationChannel(NotificationChannel):

    def send(self, message):
        formatted_message = self.formatter.format(message)
        print(f"Email send: {formatted_message}")


class SMSNotificationChannel(NotificationChannel):
    
    def send(self, message):
        formatted_message = self.formatter.format(message)
        print(f"SMS send: {formatted_message}")


class NotificationGenerator:

    def __init__(self, channels: list):
        self.channels = channels

    
    def send(self, message):
        for channel in self.channels:
            channel.send(message)


notification_channels = [
    EmailNotificationChannel(JsonFormatter()),
    SMSNotificationChannel(HTMLFormatter()),
    EmailNotificationChannel(HTMLFormatter()),
    SMSNotificationChannel(JsonFormatter()),
]


message = Message("Tanay", "realtanaymakharia@gmail.com", "Test Email", "Hi! This is for testing purpose only.")

notification_generator = NotificationGenerator(channels=notification_channels)

notification_generator.send(message)




