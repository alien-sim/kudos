from django.db import models

from kudos.apps.kudo_app.models.user import User


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
