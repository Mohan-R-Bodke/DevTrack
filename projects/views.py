from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import models
from django.http import JsonResponse

from .models import Project
from .forms import ProjectForm

from rest_framework import viewsets
from rest_framework.permissions import BasePermission, IsAuthenticated

from .serializers import ProjectSerializer


# ============================================================
# API PERMISSION
# ============================================================

class IsProjectOwnerOrReadOnly(BasePermission):

    def has_permission(self, request, view):

        return bool(
            request.user and
            request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):

        # Owner can do everything
        if obj.owner == request.user:
            return True

        # Members can only read
        return request.method in ['GET', 'HEAD', 'OPTIONS']


# ============================================================
# WEB VIEWS
# ============================================================

@login_required
def project_list(request):

    projects = Project.objects.filter(
        models.Q(owner=request.user) |
        models.Q(members=request.user)
    ).distinct().order_by('-created_at')

    return render(
        request,
        'projects/project_list.html',
        {'projects': projects}
    )


@login_required
def project_create(request):

    if request.method == 'POST':

        form = ProjectForm(
            request.POST,
            user=request.user
        )

        if form.is_valid():

            project = form.save(commit=False)

            project.owner = request.user

            project.save()

            form.save_m2m()

            # Owner is always a member
            project.members.add(request.user)

            return redirect('project_list')

    else:

        form = ProjectForm(
            user=request.user
        )

    return render(
        request,
        'projects/project_form.html',
        {'form': form}
    )


@login_required
def project_detail(request, pk):

    project = get_object_or_404(
        Project.objects.filter(
            models.Q(owner=request.user) |
            models.Q(members=request.user)
        ).distinct(),
        pk=pk
    )

    tasks = project.tasks.select_related(
        'assigned_to'
    ).order_by(
        '-created_at'
    )

    members = project.members.all().order_by(
        'username'
    )

    return render(
        request,
        'projects/project_detail.html',
        {
            'project': project,
            'tasks': tasks,
            'members': members,
        }
    )


@login_required
def project_members(request, pk):

    project = get_object_or_404(
        Project,
        pk=pk,
        owner=request.user
    )

    members = project.members.all().order_by(
        'username'
    )

    data = [
        {
            'id': member.id,
            'username': member.username
        }
        for member in members
    ]

    return JsonResponse({
        'members': data
    })


@login_required
def project_edit(request, pk):

    project = get_object_or_404(
        Project,
        pk=pk,
        owner=request.user
    )

    if request.method == 'POST':

        form = ProjectForm(
            request.POST,
            instance=project,
            user=request.user
        )

        if form.is_valid():

            form.save()

            # Owner remains a member
            project.members.add(request.user)

            return redirect(
                'project_detail',
                pk=project.pk
            )

    else:

        form = ProjectForm(
            instance=project,
            user=request.user
        )

    return render(
        request,
        'projects/project_form.html',
        {'form': form}
    )


@login_required
def project_delete(request, pk):

    project = get_object_or_404(
        Project,
        pk=pk,
        owner=request.user
    )

    if request.method == 'POST':

        project.delete()

        return redirect('project_list')

    return redirect(
        'project_detail',
        pk=project.pk
    )


# ============================================================
# PROJECT REST API
# ============================================================

class ProjectViewSet(viewsets.ModelViewSet):

    serializer_class = ProjectSerializer

    permission_classes = [
        IsAuthenticated,
        IsProjectOwnerOrReadOnly
    ]

    def get_queryset(self):

        return Project.objects.filter(
            models.Q(owner=self.request.user) |
            models.Q(members=self.request.user)
        ).distinct().order_by(
            '-created_at'
        )

    def perform_create(self, serializer):

        project = serializer.save(
            owner=self.request.user
        )

        # Creator automatically becomes a member
        project.members.add(
            self.request.user
        )