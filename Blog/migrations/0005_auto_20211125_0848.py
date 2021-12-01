# Generated by Django 3.2.5 on 2021-11-25 03:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0004_alter_post_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ManyToManyField(null=True, related_name='Author', to='Blog.Author'),
        ),
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(null=True, related_name='Author', to='Blog.Tag'),
        ),
    ]
