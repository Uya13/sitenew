from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Author (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        post_rating_dict=self.post_set.all().values("rating")
        post_sum = 0
        for rating in post_rating_dict:
            post_sum += rating["rating"]
        post_sum *= 3

        comments_rating_dict=self.user.comment_set.all().values("rating")
        comments_sum = 0
        for comment in comments_rating_dict:
            comments_sum += comment["rating"]

        post_comments_rating_dict = self.post_set.all()
        post_comments_sum = 0
        for post in post_comments_rating_dict:
            comments = post.comment_set.all().values("rating")
            for comment in comments:
                post_comments_sum += comment["rating"]

        self.rating = post_sum + comments_sum + post_comments_sum
        self.save()

    def __str__(self):
        return self.user.username


class Category (models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class PostCategory (models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)


article = "AR"
news = "NE"
post_types = [
    (article, "статья"),
    (news, "новость")
]


class Post (models.Model):
    author = models.ForeignKey("Author", on_delete=models.CASCADE)
    types = models.CharField(max_length=2, choices=post_types, default=article)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    post_category = models.ManyToManyField("Category", through=PostCategory)
    heading = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        if self.rating > 0:
            self.rating -= 1
            self.save()

    def preview(self):
        return self.text[:124]+"..."
    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

class Comment (models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    creation_datetime = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        if self.rating > 0:
            self.rating -= 1
            self.save()


#category = Category(name="политика")
#category.save()
#cap_big = Product.objects.create(name = "Монитор", price = 9999.0)

