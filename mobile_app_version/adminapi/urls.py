from django.urls import path

from mobile_app_version.adminapi import views as admin_views

urlpatterns = [
    path("apps", admin_views.AppVersioningAdminView.as_view(), name="get_and_create_app_versions"),
    path("apps/<int:pk>", admin_views.AppVersioningAdminView.as_view(), name="update_and_delete_app_versions"),
]
