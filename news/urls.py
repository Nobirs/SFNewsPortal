from django.urls import path
from .views import (NewsList,
                    PostDetail,
                    NewsSearchList,
                    PostCreate,
                    PostUpdate,
                    PostDelete,
                    update_redirect_nw_ar_if_needed,
                    delete_redirect_nw_ar_if_needed,
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
]