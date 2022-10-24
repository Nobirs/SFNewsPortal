from news.models import *

ami = User.objects.create_user('Ami')
alex = User.objects.create_user('Alex')


alex_author = Author.objects.create(author_user=alex)
ami_author = Author.objects.create(author_user=ami)


python_category = Category.objects.create(name='python')
sql_category = Category.objects.create(name='sql')
database_category = Category.objects.create(name='database')
linux_category = Category.objects.create(name='linux')
linus_torvalds_category = Category.objects.create(name='Linux Torvalds')


first_post = Post.objects.create(category_type='AR', title="Python in the Modern World", text = "Another post about Python language", post_author=alex_author)
first_post.post_category.add(python_category)
first_post.post_category.add(linus_torvalds_category)

second_post = Post.objects.create(category_type='AR', title="Linux in the Modern World", text = "Another post about Linux Torvalds(Linux - his real first name!))", post_author=alex_author)
second_post.post_category.add(linux_category)
second_post.post_category.add(linus_torvalds_category)

first_news = Post.objects.create(category_type='NW', title="Linux Torvalds - ancestor of Apple company", text = "Another post about Linux Torvalds(Linux - his real first name!))", post_author=ami_author)
first_news.post_category.add(linux_category)
first_news.post_category.add(linus_torvalds_category)


first_comment = Comment.objects.create(text='Hm.. What about Linux Torvalds?', comment_post=first_post, comment_user=ami)
second_comment = Comment.objects.create(text='It\'s Linux Torvalds again?', comment_post=second_post, comment_user=ami)
third_comment = Comment.objects.create(text='Hm.. Again Linux Torvalds?', comment_post=first_post, comment_user=alex)
fourth_comment = Comment.objects.create(text='Hm.. What about Linux Torvalds?', comment_post=first_news, comment_user=alex)


first_post.like()
first_post.like()
first_post.like()
first_post.like()
first_post.like()
first_post.like()

second_post.dislike()
second_post.dislike()
second_post.dislike()

first_news.like()
first_news.like()

first_comment.like()
first_comment.like()

second_comment.like()
second_comment.like()
second_comment.like()

third_comment.dislike()
third_comment.dislike()
third_comment.dislike()

fourth_comment.like()
fourth_comment.like()
fourth_comment.like()


ami_author.update_rating()
alex_author.update_rating()

best_author = Author.objects.order_by('-rating')[0]
print(f'{best_author.author_user.username} -> {best_author.rating}')

best_post = Post.objects.order_by('-rating')[0]
print(f'[{best_post.creation_datetime}] ({best_post.post_author.author_user.username}) {best_post.rating} {best_post.title} -> {best_post.preview()}')

best_post_comments = Comment.objects.filter(comment_post=best_post)
for comment in best_post_comments:
    print(f'[{comment.creation_datetime}] ({comment.comment_user.username}) {comment.rating} \n{comment.text}\n')