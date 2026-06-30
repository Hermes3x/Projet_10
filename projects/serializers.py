from rest_framework.serializers import ModelSerializer
from .models import Project, Contributor, Issue, Comment


class ProjectSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = [
            'id',
            'name',
            'description',
            'type',
            'author',
            'created_time',
        ]
        read_only_fields = ['author', 'created_time']


class ContributorSerializer(ModelSerializer):
    class Meta:
        model = Contributor
        fields = [
            'id',
            'user',
            'project',
        ]


class IssueSerializer(ModelSerializer):

    class Meta:
        model = Issue
        fields = [
            'id',
            'name',
            'description',
            'assignation',
            'priority',
            'tag',
            'status',
            'project',
            'author',
            'created_time',
        ]
        read_only_fields = ['author', 'created_time']


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'id',
            'uuid',
            'description',
            'issue',
            'author',
            'created_time',
        ]
        read_only_fields = ['uuid', 'author', 'created_time']
