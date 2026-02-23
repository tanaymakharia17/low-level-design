"""

Requirements:
Any user can schedule an meeting and invite others
Organiser can cancel the meeting
User have the option to select an venue, (multiple rooms and online is also a venue)
User have optional to add a meeting link for remote users
Meeting is only scheduled if all users are available on that time
Whenever an user is added to a meet or cancelled, send a notification



Classes:
Meeting
User
Observable
Observer for the notification to users
Venue abstract, then physical rooms, virtual room
Venue - multiple rooms and online venue too
MeetingScheduler controller
A Servide classes for all data type classes

"""

from __future__ import annotations
from abc import ABC, abstractmethod
import datetime
from enum import Enum


class MeetingStatusEnum(Enum):
    IN_PROGRESS = 1
    SCHEDULED = 2
    CANCELLED = 3
    COMPLETED = 4


class Observable(ABC):    
    @abstractmethod
    def notify(self):pass

class Meeting(Observable):
    id: int
    subject: str
    description: str
    start_time: datetime.datetime
    end_time: datetime.datetime
    attendees: list[User]
    organizer: User
    venue: AbstractVenue
    virtual_meet_link: str
    status: MeetingStatusEnum

    def __init__(self, id: int, subject: str, description: str, start_time, end_time, attendees, orginazer, venue, virtual_meet_link):
        self.id = id
        self.subject = subject
        self.description = description
        self.start_time = start_time
        self.end_time = end_time
        self.attendees = attendees
        self.organizer = orginazer
        self.venue = venue
        self.virtual_meet_link = virtual_meet_link
        self.status = MeetingStatusEnum.SCHEDULED
    
    def __repr__(self):
        return f'{self.subject}(id: {self.id})'
    
    def notify(self):
        for attendee in self.attendees:
            message = f"Message for {attendee}: Meeting {self} is cancelled."
            attendee.update(message)

    def cancel(self):
        self.status = MeetingStatusEnum.CANCELLED
        self.notify()




class Observer(ABC):
    @abstractmethod
    def update(self, message: str): pass


class User(Observer):
    id: int
    name: str
    meetings: list[Meeting]
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
        self.meetings = []
    
    def __repr__(self):
        return f"{self.name}(id: {self.id})"
    
    def update(self, message: str):
        print(message)

class AbstractUserService(ABC):
    @abstractmethod
    def create_user(self, id: int, name: str): pass

        
class InMemoryUserService(ABC):
    user_repository: list[User]

    def __init__(self):
        self.user_repository = []

    def create_user(self, name: str):
        id = len(self.user_repository)
        user = User(id, name)
        self.user_repository.append(user)
        return user
    
class AbstractMeetingService(ABC):
    @abstractmethod
    def create_meeting(self, id: int, name: str): pass

def generate_meet_link():
    return "https://www.meet.com"
        
class InMemoryMeetingService(ABC):
    meeting_repository: list[User]

    def __init__(self):
        self.meeting_repository = []

    def create_meeting(self, subject: str, description: str, start_time, end_time, attendees, orginazer, venue, has_meet_link=False):
        id = len(self.meeting_repository)
        virtual_meet_link = None
        if has_meet_link:
            virtual_meet_link = generate_meet_link()
        meeting = Meeting(id, subject, description, start_time, end_time, attendees, orginazer, venue, virtual_meet_link)
        self.meeting_repository.append(meeting)
        return meeting

    

class AbstractVenue(ABC):
    id: int
    meetings: list[Meeting]

    def __init__(self, id):
        self.id = id
        self.meetings = []


class PhysicalVenue(AbstractVenue):
    pass



class MeetingSchedulerController:

    def __init__(self):
        self.meeting_service = InMemoryMeetingService()
        self.user_service = InMemoryUserService()
    
    def create_meeting(self, *args, **kwargs):
        return self.create_meeting.create_user(*args, **kwargs)
    
    def create_user(self, *args, **kwargs):
        return self.user_service.create_user(*args, **kwargs)



