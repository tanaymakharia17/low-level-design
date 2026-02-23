

"""

Requirements:
1. User - profile
2. User can post a question - add tags, rating
3. Other users can comment on that question, comment under a comment
4. Theres a +1, -1 on commnt
5. Feed of the questions - multiple stratigies
6. Top contributors feature
7. User can mark any comment as solution


classes:
User - done
Question - done
AbstractComment - interface of composite pattern - done
Comment - done
FeedGenerationStrategyAbstract
Multiple strratigies - Newyest first, most related
Stackoverflow controller

"""

from __future__ import annotations


from abc import ABC, abstractmethod
import datetime

class User:
    id: int
    name: str
    questions: list[Question]
    comments: list[Comment] # optional

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.questions = []
        self.comments = []
    def __repr__(self):
        return f"{self.name}"


class Question:
    posted_by: User
    heading: str
    description: str
    comments: list[Comment]
    posted_timestamp: str
    votes: int
    tags: list[str]

    def __init__(self, posted_by, heading, description, tags):
        self.posted_by = posted_by
        self.heading = heading
        self.description = description
        self.tags = tags
        self.votes = 0
        self.posted_timestamp = datetime.datetime.now()
        self.comments = []
    
    def addComment(self, comment):
        self.comments.append(comment)


class AbstractComment(ABC):

    @abstractmethod
    def ls(self, indent=1): pass

class Comment(AbstractComment):
    posted_by: User
    description: str
    votes: int
    posted_timestamp: str
    comments: list[Comment]

    def __init__(self, posted_by: User, description: str):
        self.posted_by = posted_by
        self.description = description
        self.votes = 0
        self.posted_timestamp = datetime.datetime.now()
        self.comments = []

    def ls(self, indent=1):
        print(" "*indent + f"Comment (by: {self.posted_by}, votes: {self.votes}): {self.description}")
        for comment in self.comments:
            comment.ls(indent*2)
    
    def addComment(self, comment: Comment):
        self.comments.append(comment)
    
    def upVote(self):
        self.votes += 1
    
    def downVote(self):
        self.votes -= 1
    
    def addComment(self, comment):
        self.comments.append(comment)


class FeedGenerationStrategyAbstract(ABC):

    @abstractmethod
    def feed(self, user: User, comments: list[Comment], paginate=10):pass


class NewyestFirstStrategy(FeedGenerationStrategyAbstract):

    def feed(self, user: User, questions: list[Question], paginate=10):
        sz = len(questions)
        idx = max(0, sz - paginate)
        return questions[idx:]

class StackoverflowControlled:
    users: list[User]
    questions: list[Question]
    comments: list[Comment]

    def __init__(self):
        self.users = []
        self.questions = []
        self.comments = []
        self.feed_strategy = NewyestFirstStrategy()

    
    def generateFeed(self, user: User):
        return self.feed_strategy.feed(user, self.questions)

    def postQuestion(self, user: User, question: Question):
        user.questions.append(question)
        self.questions.append(question)
    
    def postComment(self, user: User, add_to: Comment | Question, comment: Comment):
        user.comments.append(comment)
        add_to.addComment(comment)
        self.comments.append(comment)
    
    def upVote(self, comment: Comment):
        comment.upVote()
    
    def downvote(self, comment: Comment):
        comment.downVote()
    
    def display_comments(self, question: Question):
        for comment in question.comments:
            comment.ls()
    


if __name__ == "__main__":
    # Initialize system
    system = StackoverflowControlled()

    # Create users
    alice = User(1, "Alice")
    bob = User(2, "Bob")
    charlie = User(3, "Charlie")
    dave = User(4, "Dave")
    system.users.extend([alice, bob, charlie, dave])

    # Alice posts a question
    question1 = Question(
        posted_by=alice,
        heading="What is the difference between list and tuple in Python?",
        description="I want to understand how lists and tuples differ in Python.",
        tags=["python", "data-structures"]
    )
    system.postQuestion(alice, question1)

    # Bob posts another question
    question2 = Question(
        posted_by=bob,
        heading="How does Python's GIL affect threading?",
        description="Trying to understand why threading is limited in Python.",
        tags=["python", "threading", "performance"]
    )
    system.postQuestion(bob, question2)

    # Users comment on question 1
    c1 = Comment(posted_by=bob, description="Tuples are immutable, lists are mutable.")
    c2 = Comment(posted_by=charlie, description="Lists use more memory.")
    c3 = Comment(posted_by=dave, description="Tuples can be used as dictionary keys, lists can't.")

    system.postComment(bob, question1, c1)
    system.postComment(charlie, question1, c2)
    system.postComment(dave, question1, c3)

    # Add replies to comments
    c1_1 = Comment(posted_by=alice, description="Good point, thanks!")
    c1_2 = Comment(posted_by=charlie, description="Also, tuples are slightly faster.")
    system.postComment(alice, c1, c1_1)
    system.postComment(charlie, c1, c1_2)

    c2_1 = Comment(posted_by=bob, description="Yes, because lists are dynamic.")
    system.postComment(bob, c2, c2_1)

    # Users comment on question 2
    c4 = Comment(posted_by=charlie, description="GIL prevents true parallelism in CPU-bound tasks.")
    c5 = Comment(posted_by=alice, description="But it's still useful for I/O-bound operations.")
    c6 = Comment(posted_by=dave, description="Try using multiprocessing if you want parallel CPU work.")

    system.postComment(charlie, question2, c4)
    system.postComment(alice, question2, c5)
    system.postComment(dave, question2, c6)

    # Deep reply chain
    c4_1 = Comment(posted_by=bob, description="I tried that, but ran into IPC issues.")
    c4_2 = Comment(posted_by=charlie, description="Yeah, shared memory gets tricky.")
    system.postComment(bob, c4, c4_1)
    system.postComment(charlie, c4_1, c4_2)

    # Voting on comments
    system.upVote(c1)
    system.upVote(c1)
    system.upVote(c2)
    system.downvote(c4)
    system.upVote(c5)
    system.upVote(c5)
    system.downvote(c4_2)

    # Feed generation
    print("\n📰 Feed for Dave:")
    feed = system.generateFeed(dave)
    for q in feed:
        print(f"\n📌 {q.heading} (by {q.posted_by.name})")
        print(f"   Tags: {q.tags}")
        print(f"   Description: {q.description}")
        print(f"   Votes: {q.votes}")
        print("   Comments:")
        system.display_comments(q)








# def subtract(a: str, b: str) -> int:
#     # Ensure a >= b (numerically)
#     if len(b) > len(a) or (len(a) == len(b) and b > a):
#         a, b = b, a

#     a = list(a[::-1])
#     b = list(b[::-1])

#     result = []
#     carry = 0

#     for i in range(len(a)):
#         digit_a = int(a[i])
#         digit_b = int(b[i]) if i < len(b) else 0

#         digit = digit_a - digit_b - carry
#         if digit < 0:
#             digit += 10
#             carry = 1
#         else:
#             carry = 0

#         result.append(str(digit))

#     # Remove leading zeros from the result
#     while len(result) > 1 and result[-1] == '0':
#         result.pop()

#     return int(''.join(result[::-1]))


# print(subtract("324", "1325"))