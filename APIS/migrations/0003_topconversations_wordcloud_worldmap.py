# Generated by Django 4.2.2 on 2023-07-05 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APIS', '0002_query_user_delete_userquery_query_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='TopConversations',
            fields=[
                ('keyword', models.TextField(primary_key=True, serialize=False)),
                ('top_conversations', models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='WordCloud',
            fields=[
                ('keyword', models.TextField(primary_key=True, serialize=False)),
                ('word_cloud', models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='WorldMap',
            fields=[
                ('keyword', models.TextField(primary_key=True, serialize=False)),
                ('world_map', models.JSONField()),
            ],
        ),
    ]
