from rest_framework import permissions

# DIR : 0
# CO  : 1
# RH  : 2
# SEC : 3


class IsSecretary(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return request.user.position <= 3


class IsHRM(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        else:
            return request.user.position == 2 or request.user.position == 0


class IsAccounting(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return request.user.position <= 1
