from django.db import models
import uuid
# Create your models here.

class Room(models.Model):
    id=models.UUIDField(verbose_name="Oda ID",primary_key=True,default=uuid.uuid4)
    name = models.TextField(verbose_name="Oda Adı",blank=False,null=False)

class ChatUser(models.Model):
    user=models.ForeignKey("auth.User",related_name="chat_user",verbose_name="Kullanıcı",on_delete=models.CASCADE)
    room = models.ForeignKey(Room, verbose_name="Oda",related_name="chatuser",on_delete=models.CASCADE)


class Message(models.Model):
    user=models.ForeignKey("auth.User", verbose_name="Kullanıcı", related_name="messages",on_delete=models.CASCADE)
    room=models.ForeignKey(Room, verbose_name="Oda", on_delete=models.CASCADE)
    content=models.TextField(verbose_name="Mesaj içeriği")
    created_date = models.DateTimeField(verbose_name="Saat", auto_now_add=True)