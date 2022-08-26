# Generated by Django 3.2.12 on 2022-05-23 01:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('watchlist_app', '0011_reviews_review_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='watchlist',
            name='platform',
        ),
        migrations.AddField(
            model_name='watchlist',
            name='platform',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='watchlist', to='watchlist_app.streamplatform'),
            preserve_default=False,
        ),
    ]