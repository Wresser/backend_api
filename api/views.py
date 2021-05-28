from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.contrib.auth.models import User

from django.utils import timezone

from .models import Category, Petition
from .serializers import CategoryListSerializer, PetitionListSerializer, PetitionCreateSerializer, PetitionDetailSerializer, UserListSerializer, LogoutSerializer

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=204)

class CategoryListView(APIView):

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategoryListSerializer(categories, many=True)
        return Response(serializer.data)

class PetitionListView(APIView):

    def get(self, request):
        title = request.GET.get('title', None)
        category = request.GET.get('category', None)
        creator = request.GET.get('creator', None)
        successful = request.GET.get('successful', None)
        
        
        petitions = Petition.objects.all()

        if title is not None:
            petitions = petitions.filter(title__icontains=title)

        if category is not None:
            petitions = petitions.filter(category = category)

        if creator is not None:
            creator = creator.lower()
            names = dict()
            for user in User.objects.all():
                names[user.get_full_name()] = user.id
            ids = [value for key, value in names.items() if creator in key.lower()]
            petitions = petitions.filter(creator_id__in=ids)

        if successful == "True":
            for petition in petitions:
                if not petition.HasPassed():
                    petitions = petitions.exclude(id = petition.id)
        elif successful == "False":
            for petition in petitions:
                if not (petition.IsExpired() and not petition.HasPassed()):
                    petitions = petitions.exclude(id = petition.id)          
        
        serializer = PetitionListSerializer(petitions, many=True)
        return Response(serializer.data)


class PetitionCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        request.data['creator'] = request.user.id
        petition = PetitionCreateSerializer(data=request.data)
        if petition.is_valid():
            petition.save()
        return Response(status=201)

class PetitionDetailView(APIView):

    def get(self, request, pk):
        petition = Petition.objects.get(id=pk)
        serializer = PetitionDetailSerializer(petition)
        return Response(serializer.data)

class VoteSubmitView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        petition = Petition.objects.get(id=pk)
        petition.voters.add(request.user)
        petition.save()
        return Response(status=201)

class UserListView(APIView):

    def get(self, request):
        users = User.objects.all()
        serializer = UserListSerializer(users, many=True)
        return Response(serializer.data)

class StatisticsView(APIView):

    def get(self, request):
        pet_num = Petition.objects.count()
        vote_num = 0
        for petition in Petition.objects.all():
            vote_num += petition.VoteCount()

        return Response({'petitions_number': pet_num, 'vote_number' : vote_num})
