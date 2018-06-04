from django.db import models

# Create your models here.
class Pilot(models.Model):
    # This is the pilot class which will have the information about the basic factual information
    # ...about the pilot
    # This does not contain the pilot duty time records...that's more of a time-line related 'element'
    
    
    # INCLUDE A REFERENCE OR RELATION TO THE TIMELINE
