from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.contrib.auth.models import User

from django.utils import timezone

from .models import Category, Petition
from .serializers import CategoryListSerializer, PetitionListSerializer, PetitionCreateSerializer, PetitionDetailSerializer, UserListSerializer

class CategoryListView(APIView):

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategoryListSerializer(categories, many=True)
        return Response(serializer.data)

class PetitionListView(APIView):

    def get(self, request):
        category = request.GET.get('category', None)
        creator = request.GET.get('creator', None)
        successful = request.GET.get('successful', None)

        petitions = Petition.objects.all()
        if category is not None:
            petitions = petitions.filter(category = category)
        if creator is not None:
            petitions = petitions.filter(creator = creator)
        if successful is not None:
            if successful == "True":
                for petition in petitions:
                    if not petition.HasPassed():
                        petitions = petitions.exclude(id = petition.id)
            else:
                for petition in petitions:
                    
                    if not (petition.IsExpired() and not petition.HasPassed()):
                        petitions = petitions.exclude(id = petition.id)
                        
        
        serializer = PetitionListSerializer(petitions, many=True)
        return Response(serializer.data)


class PetitionCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        petition = PetitionCreateSerializer(data=request.data)
        if petition.is_valid():
            petition.save()
        return Response(status=201)

class PetitionDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

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
