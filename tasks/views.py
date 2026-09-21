from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Task
from .forms import TaskForm
from .serializers import TaskSerializer

from rest_framework import viewsets, status
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response


# ============================================================
# TASK API PERMISSION
# ============================================================

class TaskPermission(BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):

        project = obj.project

        # Project owner has full access
        if project.owner == request.user:
            return True

        # User must be a project member
        is_member = project.members.filter(
            id=request.user.id
        ).exists()

        if not is_member:
            return False

        # Project members can view tasks
        return request.method in [
            'GET',
            'HEAD',
            'OPTIONS'
        ]


# ============================================================
# WEB VIEWS
# ============================================================

@login_required
def task_list(request):

    tasks = Task.objects.filter(
        assigned_to=request.user
    ).select_related(
        'project',
        'assigned_to'
    ).order_by(
        '-created_at'
    )

    return render(
        request,
        'tasks/task_list.html',
        {'tasks': tasks}
    )


@login_required
def task_create(request):

    if request.method == 'POST':

        form = TaskForm(
            request.POST,
            user=request.user
        )

        if form.is_valid():

            project = form.cleaned_data['project']
            assigned_to = form.cleaned_data['assigned_to']

            # Only project owner can create tasks
            if project.owner != request.user:

                form.add_error(
                    'project',
                    'Only the project owner can create tasks.'
                )

            # Assigned user must be a project member
            elif (
                assigned_to
                and not project.members.filter(
                    id=assigned_to.id
                ).exists()
            ):

                form.add_error(
                    'assigned_to',
                    'This user is not a member of the project.'
                )

            else:

                form.save()

                messages.success(
                    request,
                    'Task created successfully.'
                )

                return redirect('task_list')

    else:

        form = TaskForm(
            user=request.user
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
        pk=pk
    )

    is_owner = task.project.owner == request.user

    is_assigned = task.assigned_to == request.user

    is_project_member = task.project.members.filter(
        id=request.user.id
    ).exists()

    # Owner should also have access even if not present
    # in the members table
    if not is_project_member and not is_owner:
        return redirect('task_list')

    return render(
        request,
        'tasks/task_detail.html',
        {
            'task': task,
            'is_owner': is_owner,
            'is_assigned': is_assigned,
        }
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
            instance=task,
            user=request.user
        )

        if form.is_valid():

            project = form.cleaned_data['project']
            assigned_to = form.cleaned_data['assigned_to']

            if (
                assigned_to
                and not project.members.filter(
                    id=assigned_to.id
                ).exists()
            ):

                form.add_error(
                    'assigned_to',
                    'This user is not a member of the project.'
                )

            else:

                form.save()

                messages.success(
                    request,
                    'Task updated successfully.'
                )

                return redirect(
                    'task_detail',
                    pk=task.pk
                )

    else:

        form = TaskForm(
            instance=task,
            user=request.user
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

        messages.success(
            request,
            'Task deleted successfully.'
        )

        return redirect('task_list')

    return redirect(
        'task_detail',
        pk=task.pk
    )


@login_required
def task_status_update(request, pk):

    task = get_object_or_404(
        Task,
        pk=pk,
        assigned_to=request.user
    )

    if request.method == 'POST':

        new_status = request.POST.get('status')

        valid_statuses = [
            'TODO',
            'IN_PROGRESS',
            'COMPLETED',
        ]

        if new_status in valid_statuses:

            task.status = new_status

            task.save(
                update_fields=['status']
            )

            messages.success(
                request,
                'Task status updated successfully.'
            )

    return redirect(
        'task_detail',
        pk=task.pk
    )


# ============================================================
# TASK REST API
# ============================================================

class TaskViewSet(viewsets.ModelViewSet):

    serializer_class = TaskSerializer

    permission_classes = [
        IsAuthenticated,
        TaskPermission
    ]

    def get_queryset(self):

        return Task.objects.filter(
            project__members=self.request.user
        ).select_related(
            'project',
            'assigned_to'
        ).distinct().order_by(
            '-created_at'
        )

    def perform_create(self, serializer):

        project = serializer.validated_data.get(
            'project'
        )

        # Only project owner can create tasks
        if project.owner != self.request.user:

            raise PermissionDenied(
                'Only the project owner can create tasks.'
            )

        assigned_to = serializer.validated_data.get(
            'assigned_to'
        )

        # Assigned user must belong to project
        if (
            assigned_to
            and not project.members.filter(
                id=assigned_to.id
            ).exists()
        ):

            raise PermissionDenied(
                'Assigned user must be a member of the project.'
            )

        serializer.save()

    # ========================================================
    # PUT
    # ========================================================

    def update(self, request, *args, **kwargs):

        task = get_object_or_404(
            Task,
            pk=kwargs.get('pk')
        )

        # Only project owner can use PUT
        if task.project.owner != request.user:

            raise PermissionDenied(
                'Only the project owner can edit the complete task.'
            )

        serializer = self.get_serializer(
            task,
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    # ========================================================
    # PATCH
    # ========================================================

    def partial_update(self, request, *args, **kwargs):

        task = get_object_or_404(
            Task,
            pk=kwargs.get('pk')
        )

        # ----------------------------------------------------
        # Project owner
        # ----------------------------------------------------

        if task.project.owner == request.user:

            serializer = self.get_serializer(
                task,
                data=request.data,
                partial=True
            )

            serializer.is_valid(
                raise_exception=True
            )

            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        # ----------------------------------------------------
        # Project member
        # ----------------------------------------------------

        is_member = task.project.members.filter(
            id=request.user.id
        ).exists()

        if not is_member:

            raise PermissionDenied(
                'You are not a member of this project.'
            )

        # ----------------------------------------------------
        # Only assigned member can update status
        # ----------------------------------------------------

        if task.assigned_to != request.user:

            raise PermissionDenied(
                'Only the assigned member can update task status.'
            )

        # ----------------------------------------------------
        # Assigned member can ONLY send status
        # ----------------------------------------------------

        if set(request.data.keys()) != {'status'}:

            raise PermissionDenied(
                'Assigned members can only update task status.'
            )

        serializer = self.get_serializer(
            task,
            data=request.data,
            partial=True
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )