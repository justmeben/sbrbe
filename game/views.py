from rest_framework.views import APIView
from rest_framework.response import Response
from game.models import Game, Player
import random
from datetime import datetime
from game.serializers import GameStateSerializer, PlayerEndGameSerializer


class HealthCheckView(APIView):
    def get(self, request):
        return Response({'status': "Rabbit"})


class CreateGameView(APIView):
    def post(self, request):
        name = request.data.get('name')
        if not name:
            return Response('Name required', 400)

        game = Game.objects.create()
        player = Player.objects.create(name=name, game=game)
        game.creator = player
        game.save()

        return Response({
            'game': game.id,
            'player': player.id
        })


class JoinGameView(APIView):
    def post(self, request):
        game_id = request.data.get('game')
        if not game_id:
            return Response('Game required', 400)

        name = request.data.get('name')
        if not name:
            return Response('Name required', 400)

        try:
            game = Game.objects.get(id=game_id)
        except Game.DoesNotExist:
            return Response({'msg': 'Game not found'}, 400)

        if game.phase != 1:
            return Response({'msg': 'Game already started'}, 400)

        player = Player.objects.create(name=name, game=game)

        return Response({
            'game': game.id,
            'player': player.id
        })


class StartGameView(APIView):
    def post(self, request):
        game_id = request.data.get('game')
        if not game_id:
            return Response('Game required', 400)

        try:
            game = Game.objects.get(id=game_id)
        except Game.DoesNotExist:
            return Response({'msg': 'Game not found'}, 400)

        if game.phase != 1:
            return Response()

        player_count = Player.objects.filter(game=game).count()
        villians_count = 1 if player_count < 7 else 2
        villians_count = 3 if player_count > 11 else villians_count
        player_ids = [x for x in Player.objects.values_list('id', flat=True).filter(game=game)]
        random.shuffle(player_ids)

        Player.objects.filter(id__in=player_ids[:villians_count]).update(is_villian=True)
        game.phase = 2
        game.save()

        return Response()


class CreateVoteView(APIView):
    def post(self, request):
        game_id = request.data.get('game')
        if not game_id:
            return Response('Game required', 400)

        player_id = request.data.get('player')
        if not player_id:
            return Response('Player required', 400)

        target_id = request.data.get('target')
        if not target_id:
            return Response('target required', 400)

        try:
            game = Game.objects.get(id=game_id)
        except Game.DoesNotExist:
            return Response({'msg': 'Game not found'}, 400)

        try:
            player = Player.objects.get(id=player_id)
        except Player.DoesNotExist:
            return Response({'msg': 'Player not found'}, 400)

        if game.vote_start_time:
            return Response({'msg': 'vote already in progress'}, 400)

        game.vote_creator = player
        game.vote_start_time = datetime.now()
        game.vote_target_id = target_id
        game.save()
        player.vote = 1
        player.save()

        return Response()


class VoteView(APIView):
    def post(self, request):
        # Optional for later: validate player didnt already vote
        game_id = request.data.get('game')
        if not game_id:
            return Response('Game required', 400)

        player_id = request.data.get('player')
        if not player_id:
            return Response('Player required', 400)

        if 'is_yes' not in request.data.keys():
            return Response('is_yes required', 400)
        is_yes = request.data.get('is_yes')

        try:
            game = Game.objects.get(id=game_id)
        except Game.DoesNotExist:
            return Response({'msg': 'Game not found'}, 400)

        try:
            player = Player.objects.get(id=player_id)
        except Player.DoesNotExist:
            return Response({'msg': 'Player not found'}, 400)

        if player.vote != -1:
            return Response({'msg': 'Player already voted'}, 400)

        if player.id == game.vote_target_id:
            return Response({'msg': 'Cannot vote for self'}, 400)

        player.vote = 1 if is_yes else 0
        player.save()

        total_count = Player.objects.filter(game=game, is_alive=True).count()
        vote_count = Player.objects.filter(game=game, is_alive=True).exclude(vote=-1).count()
        vote_yes_count = Player.objects.filter(game=game, is_alive=True, vote=1).count()

        if vote_yes_count > total_count / 2 or vote_count >= total_count - 1 \
                or total_count / 2 >= (total_count - 1 - vote_count) + vote_yes_count:
            if vote_yes_count > total_count / 2:
                game.vote_target.is_alive = False
                game.vote_target.save()

                villian_count = Player.objects.filter(game=game, is_alive=True, is_villian=True).count()
                civilian_count = Player.objects.filter(game=game, is_alive=True, is_villian=False).count()

                if villian_count == 0:
                    game.phase = 3
                elif villian_count >= civilian_count:
                    game.phase = 4

            game.vote_target.last_voted_date = datetime.now()
            game.vote_target.save()
            Player.objects.filter(game=game).update(vote=-1)
            game.vote_target = None
            game.vote_start_time = None
            game.save()

        return Response()


class GameStateView(APIView):
    def post(self, request):
        game_id = request.data.get('game')
        if not game_id:
            return Response('Game required', 400)

        player_id = request.data.get('player')
        if not player_id:
            return Response('player required', 400)

        try:
            game = Game.objects.get(id=game_id)
        except Game.DoesNotExist:
            return Response({'msg': 'Game not found'}, 400)

        try:
            player = Player.objects.get(id=player_id, game=game)
        except Game.DoesNotExist:
            return Response({'msg': 'Player not found'}, 400)

        response = {"player": PlayerEndGameSerializer(player).data,
                    'game': GameStateSerializer(game, context={'is_villian': player.is_villian}).data,
                    'now': datetime.now()}

        return Response(response)