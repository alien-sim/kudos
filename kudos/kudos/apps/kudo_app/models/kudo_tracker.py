from django.db import models

from kudos.apps.kudo_app.models.user import User

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
