from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Category, Petition

class CategoryListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"

class PetitionListSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field="name", read_only=True)
    creator_name = serializers.SerializerMethodField()
    datetime_expires = serializers.SerializerMethodField()
    vote_count = serializers.SerializerMethodField()

    def get_creator_name(self, obj):
        return f"{obj.creator.first_name} {obj.creator.last_name}"

    def get_datetime_expires(self, obj):
        return obj.DateExpires()

    def get_vote_count(self, obj):
        return obj.VoteCount()

    class Meta:
        model = Petition
        exclude = ('text', 'voters', 'creator')

class PetitionDetailSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field="name", read_only=True)
    creator_name = serializers.SerializerMethodField()
    datetime_expires = serializers.SerializerMethodField()
    vote_count = serializers.SerializerMethodField()

    def get_creator_name(self, obj):
        return f"{obj.creator.first_name} {obj.creator.last_name}"

    def get_datetime_expires(self, obj):
        return obj.DateExpires()

    def get_vote_count(self, obj):
        return obj.VoteCount()

    class Meta:
        model = Petition
        exclude = ('description', 'voters')

class PetitionCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Petition
        exclude = ('datetime_created', 'voters')

class UserListSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    class Meta:
        model = User
        fields = ['id', 'full_name']