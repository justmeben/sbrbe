from rest_framework import serializers
from game.models import Game, Player


class PlayerSerializer(serializers.ModelSerializer):

    unknown = serializers.SerializerMethodField()

    class Meta:
        model = Player
        fields = ('id', 'name', 'is_alive', 'unknown', 'is_villian', 'vote', 'last_voted_date')

    def get_unknown(self, player):
        return player.is_alive


class PlayerEndGameSerializer(PlayerSerializer):

    class Meta:
        model = Player
        fields = ('id', 'name', 'is_alive', 'is_villian', 'vote', 'last_voted_date')


class GameStateSerializer(serializers.ModelSerializer):

    vote = serializers.DateTimeField(source='vote_start_time')
    vote_target = serializers.CharField(source='vote_target.name', allow_null=True)
    players = serializers.SerializerMethodField()

    class Meta:
        model = Game
        fields = ('id', 'phase', 'vote', 'vote_target', 'vote_target_id', 'vote_creator_id', 'players', 'creator_id')

    def get_players(self, game):
        players = Player.objects.filter(game=game)
        if game.phase < 3 and not self.context['is_villian']:
            return PlayerSerializer(players, many=True).data
        else:
            return PlayerEndGameSerializer(players, many=True).data
