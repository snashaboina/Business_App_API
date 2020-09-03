import pdb
from django.db import connection

from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from Core.models import Business
from Business.serializers import BusinessSerializers
from Business.permissions import role_permission
from rest_framework import generics, authentication, permissions

from rest_framework.authentication import TokenAuthentication

# Create your views here.

# def get_cursor(query):
#     try:
#         cursor = connection.cursor()
#         cursor.execute(query)
#         return cursor
#     except Exception as e:
#         logger.error("Error at get_cursor function")
#
#     return None


class BusinessViewSet(viewsets.ModelViewSet):
    """Manage Business in the database"""
    queryset = Business.objects.all().order_by('-name')
    serializer_class = BusinessSerializers

    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    @role_permission
    def list(self, request):
        # pdb.set_trace()
        print(request.user)
        cursor = connection.cursor()
        query_obj = cursor.execute('SELECT * FROM public."Core_business" ORDER BY id ASC LIMIT 100')
        query_data = cursor.fetchall()
        result = []
        query_columns = [col[0] for col in cursor.description]
        for row in query_data:
            temp_disc = dict(set(zip(query_columns, row)))
            result.append(
                {"Business Id": str(temp_disc['id']),
                 "Business Name": str(temp_disc['name']),
                 "Contact": temp_disc['contact']
                }
            )
        return Response(result)

    @role_permission
    def retrieve(self, request, pk=None):
        # pdb.set_trace()
        print(pk)
        cursor = connection.cursor()
        query_obj = cursor.execute('SELECT * FROM public."Core_business" WHERE id = %s',[pk])
        query_data = cursor.fetchone()
        result = []
        result.append(
            {"Business Id": query_data[0],
             "Business Name": query_data[1],
             "Contact": query_data[2]
            })
        return Response(result)

    @role_permission
    def update(self, request):
        # pdb.set_trace()
        cursor = connection.cursor()
        print("111")
        query_obj =  cursor.execute('update public."Core_business" set name=%s,contact=%s where id = %s returning id,name,contact,user_id',[request.data["name"], request.data["contact"], request.data["id"]])
        retrive_data = cursor.fetchone()
        return Response({'message':'Successfully updated', 'data':{'id':retrive_data[0], 'name':retrive_data[1], 'contact number':retrive_data[2]}}, status = status.HTTP_202_ACCEPTED)

    @role_permission
    def create(self, request):
        # pdb.set_trace()
        print(request.user)
        cursor = connection.cursor()
        if request.data["name"] and request.data["contact"]:
            query_obj =  cursor.execute('INSERT INTO public."Core_business" (name, contact, user_id) VALUES (%s, %s, %s) returning id,name,contact,user_id',[request.data["name"], request.data["contact"], request.data["user"]])
            retrive_data = cursor.fetchone()
            return Response({"message":"Created Successfully","data":{"id" :retrive_data[0],"name":retrive_data[1],"contact number":retrive_data[2]}},status=status.HTTP_201_CREATED)
        else:
            return Response("Please provide name and contact", status.HTTP_400_BAD_REQUEST)

    @role_permission
    def delete(self, request):
        cursor = connection.cursor()
        query_obj =  cursor.execute('DELETE FROM public."Core_business" WHERE id = %s returning id,name,contact,user_id',[request.data["id"]])
        retrive_data = cursor.fetchone()
        return Response({"message":"Deleted Successfully","data":{"id" :retrive_data[0],"name":retrive_data[1],"contact number":retrive_data[2]}},status=status.HTTP_201_CREATED)
