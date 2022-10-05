from abc import abstractmethod

from rest_framework.permissions import BasePermission


class MainPermission(BasePermission):

    def has_permission(self, request, view):
        self.groups = request.user.groups.values_list('name', flat=True)
        return bool(self.check_permission(request, view))

    @abstractmethod
    def check_permission(self, request, view):
        return False


class IsStaff(MainPermission):
    def check_permission(self, request, view):
        return bool(request.user.is_active and request.user.is_staff)


class IsAppVersioningMember(MainPermission):
    def check_permission(self, request, view):
        return bool("app_versioning_member" in self.groups and
                    IsStaff().has_permission(request, view))
