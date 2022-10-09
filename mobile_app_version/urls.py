from django.urls import path, re_path

from mobile_app_version import views

urlpatterns = [
    path('latest', views.LatestAppVersion.as_view(), name="get_latest_app_version"),
    re_path(r'info/(?P<type>(android|ios|pwa))$', views.AppInfoView.as_view(), name='get_app_info'),
]
