

from rest_framework import permissions
from django.db import connection
from Permissions.models import  CustomPermissions, CrudPermissions
from django.contrib.auth.models import User, Group
from django.core.exceptions import PermissionDenied
import pdb

def role_permission(func):
    """
    Decorator,which check whether the role have permission or not for performing specific action.
    If role has no permission to perform then it will give error.
    :param func:
    :return:
    """

    def wrapper(request, *args, **kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        FLAG = True
        if FLAG is True:
            try:
                func_name = str(func).split(' ')[1]
                print(func_name)
                # pdb.set_trace()
                # role_name = 'guest'
                # print(request.data["id"])
                cursor = connection.cursor()
                query_obj = cursor.execute('SELECT role FROM public.user_profile WHERE user_id= %s', [request.request.user.id])
                query_data = cursor.fetchone()
                role_name = query_data[0]
                group_id = Group.objects.get(name=role_name).id
                custom_perm_list = CustomPermissions.objects.get(group_id=group_id).permission_list
                permission_arr = list()
                for permission in custom_perm_list:
                    temp = CrudPermissions.objects.get(name=permission).function_name
                    permission_arr.append(temp)
                for function_list in permission_arr:
                    flag = func_name in function_list
                    if flag is True:
                        break
                if flag is True:
                    return func(request, *args, **kwargs)
                else:
                    raise PermissionDenied
            except Exception as e:
                raise PermissionDenied
        else:
            return func(request, *args, **kwargs)
    return wrapper