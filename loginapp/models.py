from django.db import models

# Create your models here.
class DeviceControl(models.Model):
    device_id = models.IntegerField(unique=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"Device {self.device_id} - {'ON' if self.status else 'OFF'}"