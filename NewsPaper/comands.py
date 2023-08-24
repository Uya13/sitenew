from news.models import *

boris = User.objects.create_user('Boris', '11111@mail.ru', '0000_cat')
arcady = User.objects.create_user('Arcady')

boris1 = Author.objects.create(user = boris)
arcady2 = Author.objects.create(user = arcady)

s1 = Category.objects.create(name = "спорт")
s2 = Category.objects.create(name = "погода")
s3 = Category.objects.create(name = "образование")
s4 = Category.objects.create(name = "политика")

p1 = Post.objects.create(author = boris1, heading = "Lol", text = "Сейчас такую шутку расскажу лол")
p2 = Post.objects.create(author = boris1, heading = "Lol3", text = "Сейчас такую шутку расскажу лол, а может и нет")
p3 = Post.objects.create(author = arcady2, types = news, heading = "Lol4", text = "Новость: новость")

PostCategory.objects.create(post = p1, category = s3)
PostCategory.objects.create(post = p1, category = s4)
PostCategory.objects.create(post = p2, category = s1)
PostCategory.objects.create(post = p3, category = s2)

c1 = Comment.objects.create(post = p1, user = boris, text = "ужас")
c2 = Comment.objects.create(post = p1, user = arcady, text = "согласен")
c3 = Comment.objects.create(post = p2, user = boris, text = "хаха")
c4 = Comment.objects.create(post = p3, user = arcady, text = "не хаха")

p1.like()
p2.like()
p3.dislike()
c1.like()
c2.like()
c3.dislike()
c4.like()

boris1.update_rating()
arcady2.update_rating()

print(Author.objects.all().order_by("-rating").values("user__username", "rating").first())

top1 = Post.objects.all().order_by("-rating").first()
print(top1.creation_datetime)
print(top1.author.user.username)
print(top1.rating)
print(top1.heading)
print(top1.preview())

for i, comment in enumerate(top1.comment_set.all().values("creation_datetime", "user__username", "rating", "text")):
    print(f'\nкомментарий №{i}')
    print(comment["creation_datetime"])
    print(comment["user__username"])
    print(comment["rating"])
    print(comment["text"])
