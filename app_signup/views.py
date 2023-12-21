# accounts/views.py
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from .serializers import UserSerializer,ImageSerializer,FileUploadSerializer
from django.core.exceptions import ObjectDoesNotExist
from .models import CustomUser,ImageModel
from rest_framework.permissions import IsAuthenticated
from django.http import Http404

@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def user_login(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')

        user = None
        if '@' in email:
            try:
                user = CustomUser.objects.get(email=email)
            except ObjectDoesNotExist:
                pass

        if not user:
            user = authenticate(email=email, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key,'email':email}, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    if request.method == 'POST':
        try:
            # Delete the user's token to logout
            request.user.auth_token.delete()
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST','GET'])
def upload_image(request):
    if request.method == 'POST':
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    images = ImageModel.objects.all()
    serializer = ImageSerializer(images, many=True)
    return Response(serializer.data)        
    
@api_view(['POST'])
def upload_file(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')

        if not uploaded_file:
            return Response({'error': 'File is empty'}, status=status.HTTP_400_BAD_REQUEST)

        allowed_extensions = ['pdf', 'jpg', 'jpeg', 'png', 'gif']  # Allowed file extensions

        file_extension = uploaded_file.name.split('.')[-1].lower()  # Get file extension
        
        if file_extension in allowed_extensions:
            serializer = FileUploadSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'file_extension': file_extension, 'message': 'File uploaded successfully'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Extension not supported'}, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['GET'])
def get_image(request, id):
    print("image_id")
    try:
        image = ImageModel.objects.get(id=id)
        serializer = ImageSerializer(image)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ImageModel.DoesNotExist:
        raise Http404("Image does not exist")


        # if not uploaded_file:
        #     return Response({'error': 'File is empty'}, status=status.HTTP_400_BAD_REQUEST)

        # file_extension = uploaded_file.name.split('.')[-1]
        # serializer = FileUploadSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

