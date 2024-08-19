from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class BlogPost(models.Model):
    title = models.CharField(max_length=60)
    slug = models.CharField(max_length=100)
    discription = models.TextField()
    create_by = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now=True)

    def get_pictures(self):
        return Picture.objects.filter(post_id=self)

    def get_pictures_one(self):
        pics = Picture.objects.filter(post_id=self)
        if pics:
            return pics[0]
        return False

    def this_user_state_like(self, user):
        like = self.likes.filter(user=user).first()
        return like.like if like else None


class Picture(models.Model):
    image = models.ImageField(upload_to='images')
    post_id = models.ForeignKey(BlogPost, on_delete=models.CASCADE)


class Like(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    like = models.BooleanField(blank=True, null=True)

    def __str__(self):
        return '{} {} {}'.format(self.user.username, self.like, self.post.title)

    class Meta:
        unique_together = ('post', 'user')


class Comments(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    message = models.CharField(max_length=250, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
