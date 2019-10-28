from django.db import models
from core import models as core_models
from users import models as user_models


# Create your models here.


class Conversation(core_models.AbstractTimeStampModel):
    """Conversation Model Definition"""

    participants = models.ManyToManyField(
        user_models.User, related_name="conversations", blank=True
    )

    def __str__(self):
        usernames = []
        for user in self.participants.all():
            usernames.append(user.username)
        return " / ".join(usernames)

    def count_messages(self):
        return self.messages.count()

    count_messages.short_description = "number of messages"

    def count_participants(self):
        return self.participants.count()

    count_participants.short_description = "number of participants"


class Message(core_models.AbstractTimeStampModel):
    message = models.TextField()
    user = models.ForeignKey(
        user_models.User, related_name="messages", on_delete=models.CASCADE
    )
    conversation = models.ForeignKey(
        Conversation, related_name="messages", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.user} says: {self.message}"
