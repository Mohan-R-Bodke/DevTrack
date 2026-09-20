from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Task
from projects.models import Project
from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .serializers import TaskSerializer

from .forms import TaskForm

@login_required
def task_list(request):

    tasks = Task.objects.filter(
        project__owner=request.user
    ).select_related(
        'project',
        'assigned_to'
    ).order_by('-created_at')

    return render(
        request,
        'tasks/task_list.html',
        {'tasks': tasks}
    )


@login_required
def task_create(request):

    if request.method == 'POST':

        form = TaskForm(request.POST)

        # Only show user's own projects
        form.fields['project'].queryset = Project.objects.filter(
            owner=request.user
        )

        if form.is_valid():

            task = form.save()

            return redirect('task_list')

    else:

        form = TaskForm()

        # Only show user's own projects
        form.fields['project'].queryset = Project.objects.filter(
            owner=request.user
        )

    return render(
        request,
        'tasks/task_form.html',
        {'form': form}
    )


@login_required
def task_detail(request, pk):

    task = get_object_or_404(
        Task,
        pk=pk,
        project__owner=request.user
    )

    return render(
        request,
        'tasks/task_detail.html',
        {'task': task}
    )


@login_required
def task_edit(request, pk):

    task = get_object_or_404(
        Task,
        pk=pk,
        project__owner=request.user
    )

    if request.method == 'POST':

        form = TaskForm(
            request.POST,
            instance=task
        )

        # Only show user's own projects
        form.fields['project'].queryset = Project.objects.filter(
            owner=request.user
        )

        if form.is_valid():

            form.save()

            return redirect(
                'task_detail',
                pk=task.pk
            )

    else:

        form = TaskForm(
            instance=task
        )

        # Only show user's own projects
        form.fields['project'].queryset = Project.objects.filter(
            owner=request.user
        )

    return render(
        request,
        'tasks/task_form.html',
        {'form': form}
    )


@login_required
def task_delete(request, pk):

    task = get_object_or_404(
        Task,
        pk=pk,
        project__owner=request.user
    )

    if request.method == 'POST':
        task.delete()
        return redirect('task_list')

    return render(
        request,
        'tasks/task_confirm_delete.html',
        {'task': task}
    )



class TaskViewSet(viewsets.ModelViewSet):

    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return Task.objects.filter(
            project__owner=self.request.user
        ).order_by('-created_at')