from django.conf.urls import url

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from train.consumers import TrainConsumer
from test_model.consumers import TestConsumer
from labels.consumers import LabelsConsumer

application = ProtocolTypeRouter({

    # WebSocket chat handler
    "websocket": AuthMiddlewareStack(
        URLRouter([
            url(r"^ws/train$", TrainConsumer),
            url(r"^ws/test$", TestConsumer),
            url(r"^ws/labels$", LabelsConsumer),
        ])
    ),

})
