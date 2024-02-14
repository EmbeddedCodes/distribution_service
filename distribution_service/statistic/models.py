
from django.db import models
from helper.model import Meta


class EndpointPerformance(Meta):
    """
    The EndpointPerformance model extends the Meta class, 
    capturing performance metrics for various endpoints within the application. 
    It stores the endpoint's path and its response time in seconds, 
    aiding in monitoring and optimizing application performance. 
    Each instance includes a timestamp (inherited from Meta) marking when the data was recorded, 
    providing a historical view of endpoint efficiency over time. 
    This model is crucial for identifying bottlenecks and improving 
    user experience by facilitating targeted performance enhancements.
    """
    endpoint = models.CharField(
        max_length=255, help_text='The called endpoint')
    response_time = models.FloatField(help_text="Response time in seconds")

    def __str__(self):
        return f"{self.endpoint} - {self.response_time}s on {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
