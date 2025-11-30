from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from .models import Item
from .serlializers import ItemSerializer, RegisterSerializer, LoginSerializer
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.response import Response
# from rest_framework import status, serializers
# from rest_framework.permissions import IsAuthenticated, AllowAny
# from django.contrib.auth import authenticate
# from rest_framework_simplejwt.tokens import RefreshToken
# from .models import Item
# from .serlializers import ItemSerializer, RegisterSerializer, LoginSerializer

# register user
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User registered successfully"}, status=201)
    return Response(serializer.errors, status=400)

# login user
@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data['username']
    password = serializer.validated_data['password']

    user = authenticate(username=username, password=password)
    if user:
        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        })
    return Response({"error": "Invalid credentials"}, status=400)

# add items (POST)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_items(request):
    serializer = ItemSerializer(data=request.data)

    if Item.objects.filter(**request.data).exists():
        raise serializers.ValidationError("This item already exists")

    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Data added successfully"}, status=201)
        # return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

# view items (GET)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_items(request):
    if request.query_params:
        items = Item.objects.filter(**request.query_params.dict())
    else:
        items = Item.objects.all()

    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)

# update item (PUT)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_items(request, pk):
    try:
        item = Item.objects.get(pk=pk)
    except Item.DoesNotExist:
        return Response({"error": "Item not found"}, status=404)

    serializer = ItemSerializer(item, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Data updated successfully"}, status=201)
    return Response(serializer.errors, status=400)

# delete item (DELETE)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_items(request, pk):
    try:
        item = Item.objects.get(pk=pk)
    except Item.DoesNotExist:
        return Response({"error": "Item not found"}, status=404)

    item.delete()
    return Response({"message": "Item deleted successfully"}, status=204)


# class stud(APIView):
#         permission_classes = (IsAuthenticated, )
#         def get(self, request):
#             items = Item.objects.all()
#             serializer = ItemSerializer(items, many=True)
#             return Response(serializer.data)
            
# @api_view(['GET'])
# def ApiOverview(request):
#     api_urls = {
#         'all_items': '/',
#         'Search by Category': '/?category=category_name',
#         'Search by Subcategory': '/?subcategory=category_name',
#         'Add': '/create',
#         'Update': '/update/pk',
#         'Delete': '/item/pk/delete'
#     }

#     return Response(api_urls)

# @api_view(['POST'])
# def add_items(request):
#     item = ItemSerializer(data=request.data)

#     if Item.objects.filter(**request.data).exists():
#         raise serializers.ValidationError('This data already exists')

#     if item.is_valid():
#         item.save()
#         return Response(item.data)
#     else:
#         return Response(status=status.HTTP_404_NOT_FOUND)

# @api_view(['GET'])
# def view_items(request):
    
#     if request.query_params:
#         items = Item.objects.filter(**request.query_params.dict())
#     else:
#         items = Item.objects.all()

#     if items:
#         serializer = ItemSerializer(items, many=True)
#         return Response(serializer.data)
#     else:
#         return Response(status=status.HTTP_404_NOT_FOUND)

# @api_view(['POST'])
# def update_items(request, pk):
#     item = Item.objects.get(pk=pk)
#     data = ItemSerializer(instance=item, data=request.data)

#     if data.is_valid():
#         data.save()
#         return Response(data.data)
#     else:
#         return Response(status=status.HTTP_404_NOT_FOUND)

# @api_view(['DELETE'])
# def delete_items(request, pk):
#     item = status=status.get_object_or_404(Item, pk=pk)
#     item.delete()
#     return Response(status=status.HTTP_202_ACCEPTED)