from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Project

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .serializers import ProjectSerializer

from .forms import ProjectForm

@login_required
def project_list(request):

    projects = Project.objects.filter(
        owner=request.user
    ).order_by('-created_at')

    return render(
        request,
        'projects/project_list.html',
        {'projects': projects}
    )


@login_required
def project_create(request):

    if request.method == 'POST':

        form = ProjectForm(request.POST)

        if form.is_valid():

            project = form.save(commit=False)

            project.owner = request.user

            project.save()

            return redirect('project_list')

    else:

        form = ProjectForm()

    return render(
        request,
        'projects/project_form.html',
        {'form': form}
    )

@login_required
def project_detail(request, pk):

    project = get_object_or_404(
        Project,
        pk=pk,
        owner=request.user
    )

    return render(
        request,
        'projects/project_detail.html',
        {'project': project}
    )

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
            instance=project
        )

        if form.is_valid():

            form.save()

            return redirect(
                'project_detail',
                pk=project.pk
            )

    else:

        form = ProjectForm(
            instance=project
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

    return render(
        request,
        'projects/project_confirm_delete.html',
        {'project': project}
    )


class ProjectViewSet(viewsets.ModelViewSet):

    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return Project.objects.filter(
            owner=self.request.user
        ).order_by('-created_at')

    def perform_create(self, serializer):

        serializer.save(
            owner=self.request.user
        )