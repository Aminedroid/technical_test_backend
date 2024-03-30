from rest_framework.views import APIView
from .serializers import UserSerializer
from django.http.response import JsonResponse, Http404
from .models import User
from rest_framework.response import Response


class UserView(APIView):

    # Get a user if pk exists, else get all users
    def get(self, request, pk=None):
        if pk:
            data = self.get_user(pk)
            serializer = UserSerializer(data)
        else:
            data = User.objects.all()
            serializer = UserSerializer(data, many=True)
        return Response(serializer.data)

    # Create new user
    def post(self, request):
        data = request.data
        serializer = UserSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse('User created successfully', safe=False)
        return JsonResponse('User creation failed', safe=False)

    # Update existing user's data
    def put(self, request, pk=None):
        user_to_update = User.objects.get(user_id=pk)
        serializer = UserSerializer(user_to_update, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse('User updated successfully', safe=False)
        return JsonResponse('User update failed', safe=False)

    def delete(self, request, pk=None):
        user_to_delete = User.objects.get(user_id=pk)
        user_to_delete.delete()
        return JsonResponse('User deleted successfully', safe=False)

    def get_user(self, pk):
        try:
            user = User.objects.get(user_id=pk)
            return user
        except User.DoesNotExist:
            raise Http404
