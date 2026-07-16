from rest_framework.serializers import ModelSerializer, ValidationError
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

    def validate(self, attrs):
        # Le projet vient du corps de la requête (création) ou de l'issue existante (mise à jour partielle)
        project = attrs.get('project') or getattr(self.instance, 'project', None)
        assignee = attrs.get('assignation')

        # On ne peut assigner l'issue qu'à un contributeur du projet concerné
        if assignee is not None and project is not None:
            is_contributor = Contributor.objects.filter(
                user=assignee, project=project
            ).exists()
            if not is_contributor:
                raise ValidationError({
                    'assignation': "L'utilisateur assigné doit être contributeur du projet."
                })

        return attrs


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
