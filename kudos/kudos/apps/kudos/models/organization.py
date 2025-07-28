from django.db import models


class Organization(models.Model):


    name = models.CharField(
        max_length=100
    )

    class Meta:
        db_table = "organization"
        verbose_name = "Organization"
        verbose_name_plural = "Organizations"

    def __str__(self):
        """
        Returns the string representation Organization
        """
        return self.name