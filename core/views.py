from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, get_object_or_404, DestroyAPIView, \
    UpdateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, AllowAny

from .models import Post
from .serializers import PostSerializer

from core.models import User

from .decorators import allowed_users, unauthenticated_user
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly


def HandleRegister(request):
    if request.user.is_authenticated:
        return redirect('home')
    elif request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        if pass1 == pass2:
            customer = User.objects.create_user(username, email, pass1)
            customer.first_name = first_name
            customer.last_name = lastname
            customer.save()
            group = Group.objects.get(name='customer')
            customer.groups.add(group)
            return redirect('register')

    return render(request, 'registration/signup.html')

@unauthenticated_user
def HandleLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'registration/login.html')


def LogOut(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def HOME(request):
    return render(request, 'home.html')


class CreatePostAPIView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class ListPostAPIView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (AllowAny,)


class GetAuthorAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get(self, request, pk):
        if pk:
            post_owner = get_object_or_404(User, pk=pk)
            user_posts = Post.objects.filter(author=post_owner)
            serializer = PostSerializer(user_posts, many=True)
            return Response(data=serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class DeletePostsAPIView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAdminOrReadOnly, )

    def delete(self, request, pk):
        if pk:
            Post.objects.all().delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class DestroyDetailPostAPIView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def destroy(self, request, pk, uuid):
        if pk and uuid:
            post_owner = get_object_or_404(User, pk=pk)
            user_posts = Post.objects.filter(author=post_owner, uuid=uuid)
            user_posts.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UpdatePostAPIView(UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def update(self, request, pk, uuid):
        if pk and uuid:
            post_owner = get_object_or_404(User, pk=pk)
            user_posts = Post.objects.filter(author=post_owner, uuid=uuid)
            if user_posts:
                title = request.POST.get('title')
                content = request.POST.get('content')
                print(title + content)
            user_posts.update(title=title, content=content)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
