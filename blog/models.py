from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class PostLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

class CommentLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.ForeignKey('blog.Comment', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'comment')


# Класс модели записи в блоге
class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts')
    likes = models.ManyToManyField(User,
                                   related_name='liked_posts',
                                   blank=True)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.PUBLISHED)
    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title


# Класс камментариев в к записям
class Comment(models.Model):
    post_comment = models.ForeignKey(Post,
                                     on_delete=models.CASCADE,
                                     related_name='post_comment')
    author_comment = models.ForeignKey(User,
                                       on_delete=models.CASCADE,
                                       related_name='author_comment')
    body_comment = models.CharField(max_length=250)
    publish_comment = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User,
                                   related_name='liked_comments',
                                   blank=True)
    reply_comment = models.ForeignKey('self', on_delete=models.CASCADE,
                                      null=True,
                                      blank=True,
                                      related_name='reply')

    class Meta:
        ordering = ['publish_comment']
        indexes = [
            models.Index(fields=['publish_comment']),
        ]

    def __str__(self):
        return f'Comment by {self.author_comment} on {self.body_comment}'

