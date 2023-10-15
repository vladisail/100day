from django.contrib import admin
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status']
    list_filter = ['status', 'created', 'publish', 'author']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'post_comment', 'author_comment', 'body_comment', 'publish_comment']
    list_filter = ['publish_comment']
    search_fields = ['body_comment', 'author_comment_username']
    date_hierarchy = 'publish_comment'
    ordering = ['-publish_comment']
    actions = ['delete_selected_comments']  # Добавляем наше действие удаления комментариев

    def delete_selected_comments(self, request, queryset):
        queryset.delete()

    delete_selected_comments.short_description = "Удалить выбранные комментарии"
