from django.urls import re_path, path, include
from rest_framework.routers import DefaultRouter, SimpleRouter
from . import views
#from django.conf.urls import re_path
#from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

# import Optimade_ViewSet
# from .views import Atomss_ViewSet
# from .views import MatViewSet,JARVIS_DFT_ViewSet,Atomss_ViewSet

# Create a router and register our viewsets with it
router = DefaultRouter()
router = SimpleRouter()
router.register(r"jarvisdft/v1/structures", views.Optimade_ViewSet, "Optimade")
# router.register(r"v1/structures/?P<pk>[^/.]+", views.Optimade_ViewSet,'Optimade_details')
# router.register(r"v1/xyz", views.jarvisdft_info,'Optimade')
# router.register(r"v1/info/structures", views.jarvisdft_info,'info')
# urlpatterns = router.urls

# """
# urlpatterns += [
urlpatterns = [
    re_path(r"^", include(router.urls), name="xyz"),
    # (router.register(r"v1/structures", views.Optimade_ViewSet,basename='Optimade')).urls,
    re_path(
        r"^jarvisdft/v1/info/structures/$",
        views.jarvisdft_info,
        name="struct_info",
    ),
    re_path(r"^jarvisdft/v1/info/$", views.jarvisdft_general_info, name="info"),
    re_path(r"^jarvisdft/v1/links/$", views.jarvisdft_links, name="links"),
    re_path(r"^jarvisdft/v1/versions/$", views.jarvisdft_versions, name="version"),
    re_path(r"^jarvisdft/versions/$", views.jarvisdft_versions, name="version"),
]
# """
