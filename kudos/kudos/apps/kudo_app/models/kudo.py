from datetime import timedelta
from django.core.exceptions import ValidationError
from django.db import models

from kudos.apps.kudo_app.models.user import User
from kudos.apps.kudo_app.utility import get_week_start
from kudos.apps.kudo_app.models.kudo_tracker import WeeklyKudoTracker


class Kudo(models.Model):
    """
    Representing Kudo from one user to another
    """

    sender = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='sent_kudos'
    )
    receiver = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='received_kudos'
    )
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "kudo"
        verbose_name = "Kudo"
        verbose_name_plural = "Kudos"

    def __str__(self):
        return f"{self.sender} => {self.receiver}"
    
    @classmethod
    def kudo_sent_this_week(cls, sender, receiver) -> bool:
        week_start = get_week_start()
        next_week_start = week_start + timedelta(days=7)

        return cls.objects.filter(
            sender_id=sender,
            receiver_id=receiver,
            created_at__date__gte=week_start,
            created_at__date__lt=next_week_start
        ).exists()
    
    @classmethod
    def send_kudo(cls, sender: int, receiver: int, message: str) -> None:
        tracker =  WeeklyKudoTracker.get_or_create_weekly_tracker(sender)
        if tracker.kudos_given >= 3:
            raise ValidationError(
                "Kudo Limit exceeded."
            )
        cls.objects.create(
            sender_id=sender,
            receiver_id=receiver,
            message=message
        )

        tracker.kudos_given += 1
        tracker.save()


