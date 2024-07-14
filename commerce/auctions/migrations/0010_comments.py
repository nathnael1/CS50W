# Generated by Django 5.0.6 on 2024-07-14 17:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_winners_auction_title_alter_winners_auction_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('auction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commented', to='auctions.auctions')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commenter', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
