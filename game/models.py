from django.db import models


class Game(models.Model):
    phase = models.IntegerField(default=1)
    vote_target = models.ForeignKey("Player", null=True, blank=True,
                                    on_delete=models.DO_NOTHING, related_name='vote_target_at')
    vote_start_time = models.DateTimeField(null=True, blank=True)


class Player(models.Model):
    game = models.ForeignKey(Game, null=False, blank=False, on_delete=models.DO_NOTHING, related_name='player')
    name = models.CharField(max_length=128, null=False, blank=False)
    is_villian = models.BooleanField(default=False)
    is_alive = models.BooleanField(default=True)
    vote = models.IntegerField(default=-1)