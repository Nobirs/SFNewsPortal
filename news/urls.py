from django.urls import path
from .views import (NewsList,
                    PostDetail,
                    NewsSearchList,
                    PostCreate,
                    PostUpdate,
                    PostDelete,
                    CategoryPostsList,
                    subscribe,
                    add_new_author,
                    )


urlpatterns = [
    path('', NewsList.as_view(), name='home'),
    path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('search/', NewsSearchList.as_view(), name='search'),

    # See PostCreate.form_valid method for more info
    path('create_news/', PostCreate.as_view(), name='create_news'),
    path('create_article/', PostCreate.as_view(), name='create_article'),

    path('<int:pk>/update/', PostUpdate.as_view(), name='update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='delete'),

    path('category/<int:pk>/', CategoryPostsList.as_view(), name='category_posts'),

    path('category/<int:pk>/subscribe/', subscribe, name='subscribe'),

    path('add_new_author/', add_new_author, name='add_new_author'),
]