import json
from re import U
from .models import Message
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.utils import timezone
from django.contrib.auth.models import User
class ChatConsumer(WebsocketConsumer):
    def connect(self):
        user = self.scope['user']
        user.last_login = timezone.now()
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = self.scope["user"]
        user.last_login = timezone.now()
        m  = Message.objects.create(content=message,room_id=self.room_name,user=user)
        print(f"********-- {user} --******** {message}")
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                "user":user.username,
                "created_date":f"{m.created_date.hour}:{m.created_date.minute}"
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        user = event['user']
        user.last_login = timezone.now()
        created_date = event['created_date']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            "user": user,
            "created_date" : created_date
        }))