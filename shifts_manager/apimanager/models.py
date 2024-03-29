from django.db import models


# Create your models here.
class Worker(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.id} - {self.name}"


class Shift(models.Model):
    class ShiftTimes(models.TextChoices):
        FIRST = "00:00"
        SECOND = "08:00"
        THIRD = "16:00"

    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    shift_date = models.DateField("Shift Date")
    shift_start = models.CharField(max_length=5, choices=ShiftTimes.choices)
    shift_end = models.CharField(
        max_length=5, choices=ShiftTimes.choices, blank=True, null=True
    )

    def __str__(self):
        return f"Shift by {self.worker.id} - {self.worker.name} at {self.shift_date} from {self.shift_start} to {self.shift_end}"
