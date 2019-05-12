from django.conf.urls import url

from filesapp import views


urlpatterns = [
    url(r'^(?P<archived>[\w-]+)/$', views.FileRepoView.as_view(),
        name='getfiles'),
]
