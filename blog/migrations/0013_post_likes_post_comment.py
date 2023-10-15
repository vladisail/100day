# Generated by Django 4.2.5 on 2023-10-02 11:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0012_delete_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='likes_post',
            field=models.ManyToManyField(blank=True, related_name='post_likes', to=settings.AUTH_USER_MODEL, verbose_name='Лайки поста'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body_comment', models.CharField(max_length=250)),
                ('publish_comment', models.DateTimeField(default=django.utils.timezone.now)),
                ('author_comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_comment', to=settings.AUTH_USER_MODEL)),
                ('likes_comment', models.ManyToManyField(blank=True, related_name='comment_likes', to=settings.AUTH_USER_MODEL, verbose_name='Лайки коммента')),
                ('post_comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_comment', to='blog.post')),
                ('reply_comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reply', to='blog.comment')),
            ],
            options={
                'ordering': ['-publish_comment'],
                'indexes': [models.Index(fields=['-publish_comment'], name='blog_commen_publish_b65f33_idx')],
            },
        ),
    ]
