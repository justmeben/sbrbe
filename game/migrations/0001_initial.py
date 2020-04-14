# Generated by Django 3.0.5 on 2020-04-11 16:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phase', models.IntegerField(default=1)),
                ('vote_yes_count', models.IntegerField(default=-1)),
                ('vote_start_time', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('is_villian', models.BooleanField(default=False)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='player', to='game.Game')),
            ],
        ),
        migrations.AddField(
            model_name='game',
            name='vote_target_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='vote_target_at', to='game.Player'),
        ),
    ]