from django.db import models
from datetime import date, timedelta

from kudos.apps.kudo_app.models.user import User
from kudos.apps.kudo_app.utility import get_week_start

class WeeklyKudoTracker(models.Model):
    """
    Tracks the number of kudos a user has given during a specific week.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='kudo_tracker'
    )
    week_start = models.DateField()  # Start date of the week
    kudos_given = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "weekly_kudo_tracker"
        verbose_name = "Kudo tracker"
        verbose_name_plural = "Kudo tracker"
        unique_together = ('user', 'week_start')

    def __str__(self):
        return f"{self.id}"
    
    
    @classmethod
    def get_or_create_weekly_tracker(cls, user):
        week_start = get_week_start()
        tracker, _ = WeeklyKudoTracker.objects.get_or_create(
            user_id=user,
            week_start=week_start
        )
        return tracker


