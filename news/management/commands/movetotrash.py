from django.core.management.base import BaseCommand
from news.models import Post, Category


class Command(BaseCommand):
    help = """Move all posts which includes specific --word.
                Required argument: 
                            --word=<part of article/news title>"""

    def add_arguments(self, parser):
        parser.add_argument('--word', type=str)

    def handle(self, *args, **options):
        try:
            trash_category = Category.objects.get(name='trash_category')
        except Category.DoesNotExist:
            self.stdout.write(self.style.ERROR("[ERROR] Cannot find category with name 'trash_category'..."))
            return

        future_trash_posts = Post.objects.filter(title__icontains=options['word'])

        for post in future_trash_posts:
            self.stdout.write(self.style.NOTICE(f"Post {post} will be added to trash_category"))

        confirm = input(f"Are you sure you want to move all posts below to trash_category?(yes/no): ") == 'yes'

        if confirm:
            for post in future_trash_posts:
                if trash_category not in post.post_category.all():
                    post.post_category.add(trash_category)
                    self.stdout.write(self.style.SUCCESS(f"Post {post} was added to trash_category..."))
                else:
                    self.stdout.write(self.style.WARNING(f"Post {post} already have trash_category..."))
        else:
            self.stdout.write(self.style.ERROR("I know - you don't wanna delete those posts..."))