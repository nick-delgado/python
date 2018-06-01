from django.db import models

# Create your models here.
class Winds(models.Model):
    # This will have winds aloft...be it seasonal or current
    # retrieve from Redis database
    # ...what methods or variables to assign here? Is there really anything?
    # ...We don't need to save data on two separate detabases
