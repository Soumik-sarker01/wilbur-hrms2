from django.db import models

class TaskEntry(models.Model):
    date = models.DateField()
    order_id = models.CharField(max_length=100)
    profile = models.CharField(max_length=100)
    client = models.CharField(max_length=100, default="N/A")
    total_design = models.PositiveIntegerField()
    previously_done = models.PositiveIntegerField()
    today_target = models.PositiveIntegerField()
    status = models.CharField(max_length=50, default="In Progress")  # <-- Default added here
    remarks = models.TextField(blank=True, null=True)
    due_date = models.DateField()

    # Designer 1
    designer1 = models.CharField(max_length=100)
    designer1_target = models.PositiveIntegerField()
    designer1_done = models.PositiveIntegerField()

    # Designer 2
    designer2 = models.CharField(max_length=100)
    designer2_target = models.PositiveIntegerField()
    designer2_done = models.PositiveIntegerField()

    # Designer 3
    designer3 = models.CharField(max_length=100)
    designer3_target = models.PositiveIntegerField()
    designer3_done = models.PositiveIntegerField()

    # Designer 4
    designer4 = models.CharField(max_length=100)
    designer4_target = models.PositiveIntegerField()
    designer4_done = models.PositiveIntegerField()

    done_today = models.PositiveIntegerField()
    design_left = models.IntegerField()
    total_done = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.date} - {self.order_id}"
