from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import models

from projects.models import Project
from tasks.models import Task


@login_required
def dashboard(request):

    # Projects owned by the user OR projects where the user is a member
    projects = Project.objects.filter(
        models.Q(owner=request.user) |
        models.Q(members=request.user)
    ).distinct()

    # Tasks assigned to the logged-in user
    # This includes tasks from projects owned by others
    tasks = Task.objects.filter(
        assigned_to=request.user
    ).select_related(
        'project',
        'assigned_to'
    ).order_by(
        'due_date'
    )

    context = {

        # Project statistics
        'total_projects': projects.count(),

        'active_projects': projects.filter(
            status='ACTIVE'
        ).count(),

        'completed_projects': projects.filter(
            status='COMPLETED'
        ).count(),


        # Assigned task statistics
        'total_tasks': tasks.count(),

        'todo_tasks': tasks.filter(
            status='TODO'
        ).count(),

        'in_progress_tasks': tasks.filter(
            status='IN_PROGRESS'
        ).count(),

        'completed_tasks': tasks.filter(
            status='COMPLETED'
        ).count(),


        # Upcoming tasks assigned to the user
        'upcoming_tasks': tasks.exclude(
            status='COMPLETED'
        ).order_by(
            'due_date'
        )[:5],
    }

    return render(
        request,
        'dashboard.html',
        context
    )