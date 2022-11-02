from django.urls import path
from .views import (NewsList,
                    PostDetail,
                    NewsSearchList,
                    PostCreate,
                    PostUpdate,
                    update_redirect_nw_ar_if_needed,
                    delete_redirect_nw_ar_if_needed,
                    )


urlpatterns = [
    path('', NewsList.as_view(), name='home'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search/', NewsSearchList.as_view(), name='search'),

    # See PostCreate.form_valid method for more info
    path('create/', PostCreate.as_view(), name='create'),

    path('<int:pk>/update/', update_redirect_nw_ar_if_needed, name='update'),
    path('<int:pk>/delete/', delete_redirect_nw_ar_if_needed, name='delete'),
]