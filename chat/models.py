from django.db import models
import uuid
# Create your models here.

class Room(models.Model):
    id=models.UUIDField(verbose_name="Oda ID",primary_key=True,default=uuid.uuid4)
    first_user = models.ForeignKey("auth.user", related_name="room_first", on_delete=models.CASCADE)
    second_user = models.ForeignKey("auth.user", related_name="room_second", on_delete=models.CASCADE)
    



class Message(models.Model):
    user=models.ForeignKey("auth.User", verbose_name="Kullanıcı", related_name="messages",on_delete=models.CASCADE)
    room=models.ForeignKey(Room, verbose_name="Oda", on_delete=models.CASCADE)
    content=models.TextField(verbose_name="Mesaj içeriği")
    created_date = models.DateTimeField(verbose_name="Saat", auto_now_add=True)