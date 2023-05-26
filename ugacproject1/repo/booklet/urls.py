from django.urls import path
from booklet.views import LoginPageView, SignupPageView, BookletListView, BookletUploadView, BookletDeleteView

urlpatterns = [
    path('', LoginPageView.as_view(), name='login'),
    path('signup/', SignupPageView.as_view(), name='signup'),
    path('booklets/', BookletListView.as_view(), name='booklet_list'),
    path('booklets/upload/', BookletUploadView.as_view(), name='booklet_upload'),
    path('booklets/delete/<int:pk>/', BookletDeleteView.as_view(), name='booklet_delete'),
]
