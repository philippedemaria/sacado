from tool.models import Player
from django.db.models.signals import post_save
#from asgiref.sync import async_to_sync
#from channels.layers import get_channel_layer
from django.dispatch import receiver
from tool.models import Generate_quizz


# @receiver(post_save, sender=Player)
# def announce_new_player(sender, instance, created, **kwargs):
#     if created:
#         channel_layer = get_channel_layer()
#         async_to_sync(channel_layer.group_send)(
#             "gossip", {"type": "player.gossip",
#                        "event": "New Player",
#                        "player": instance.student.user.first_name
#                        })


@receiver(post_save, sender=Generate_quizz)
def get_new_player(sender, **kwargs):
	if kwargs['update_fields'] :
		print("recu")


 