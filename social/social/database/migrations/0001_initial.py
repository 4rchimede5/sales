# Generated by Django 2.2.12 on 2023-03-29 15:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Follower_date',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Following_date',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.ImageField(upload_to='', verbose_name='Post image')),
                ('caption_text', models.CharField(default='', max_length=100, verbose_name='caption')),
                ('likes', models.IntegerField(default=0, verbose_name='likes')),
                ('likers', models.CharField(default='', max_length=50, verbose_name='likers')),
            ],
        ),
        migrations.CreateModel(
            name='Following',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('handle', models.CharField(max_length=50, verbose_name='social handle')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('date', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pull_date', to='database.Following_date')),
                ('time', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pull_time', to='database.Following_date')),
            ],
        ),
        migrations.CreateModel(
            name='Follower',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('handle', models.CharField(max_length=50, verbose_name='social handle')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('date', models.ForeignKey(blank=True, db_column='date', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pl_date', to='database.Follower_date')),
                ('time', models.ForeignKey(blank=True, db_column='time', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pl_time', to='database.Follower_date')),
            ],
        ),
    ]
