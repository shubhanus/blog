from __future__ import unicode_literals
from time import timezone
import datetime
from django.db import models
from django.contrib import admin


class Posts(models.Model):
    post_title = models.CharField(max_length=20)
    post_text = models.TextField(max_length=1000)

    def __str__(self):
        return self.post_title
    post_date = models.DateTimeField('Post Date Update')

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Comments(models.Model):

    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    comment = models.TextField(max_length=200)

    def __str__(self):
        return self.comment
    user_name = models.CharField(max_length=30)
    comment_date = models.DateTimeField('Comment Date Update')


# class Register_login(models.Model):
#         user_name = models.CharField(max_length=20)
#
#         def __str__(self):
#             return self.user_name
#         password = models.CharField(max_length=10)
#         email = models.CharField(max_length=20)


class CommentsInline(admin.TabularInline):
    model = Comments
    extra = 2


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields' : ['post_title']}),
        ('Post', {'fields' : ['post_text'], 'classes': ['collapse']}),
        ('Date Information', {'fields' : ['post_date'], 'classes': ['collapse']}),
    ]
    inlines = [CommentsInline]
    list_display = ('post_title', 'post_date')
    list_filter = ['post_date']
    search_fields = ['post_title']

admin.site.register(Posts, QuestionAdmin)
