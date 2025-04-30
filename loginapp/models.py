from django.db import models

# Create your models here.
class DeviceControl(models.Model):
    device_id = models.IntegerField(unique=True)
    status = models.BooleanField(default=False)
    last_triggered = models.DateTimeField(null=True, blank=True)  # ⏱️ NEW: logs ESP32 action time

    def __str__(self):
        return f"Device {self.device_id}: {'ON' if self.status else 'OFF'}"