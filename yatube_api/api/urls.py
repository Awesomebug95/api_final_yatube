from django.urls import path, include

from rest_framework import routers

from api.views import PostViewSet, CommentViewSet, FollowViewSet, GroupViewSet


router_v1 = routers.DefaultRouter()
router_v1.register(r'posts', PostViewSet, basename='posts')
router_v1.register(r'groups', GroupViewSet, basename='groups')
router_v1.register(r'posts/(?P<post_id>\d+)/comments',
                   CommentViewSet,
                   basename='comments'
                   )
router_v1.register(r'follow', FollowViewSet, basename='follows')

urlpatterns = [

    path('v1/', include(router_v1.urls)),
    path('v1/', include('djoser.urls.jwt')),

]
