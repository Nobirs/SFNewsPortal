from django.core.management.base import BaseCommand
from news.models import Post, Category


class Command(BaseCommand):
    help = """Required argument: 
                --cateogory=<category_name>"""

    def add_arguments(self, parser):
        parser.add_argument('--category', type=str)

    def handle(self, *args, **options):
        confirm = input(f"Are you sure you want to delete all posts in category {options['category']}?(yes/no): ") == 'yes'

        if confirm:
            try:
                category = Category.objects.get(name=options['category'])
                posts = Post.objects.filter(post_category=category)
                for post in posts:
                    post_repr = str(post)
                    post.delete()
                    self.stdout.write(self.style.SUCCESS(f"Post {post_repr} was deleted..."))
            except Category.DoesNotExist:
                self.stdout.write(f"Error!!! Can't find category f{options['category']}")
        else:
            self.stdout.write(self.style.ERROR("You don't wanna delete those posts..."))