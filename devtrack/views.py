from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from projects.models import Project
from tasks.models import Task


@login_required
def dashboard(request):

    projects = Project.objects.filter(
        owner=request.user
    )

    tasks = Task.objects.filter(
        project__owner=request.user
    )

    context = {
        'total_projects': projects.count(),

        'active_projects': projects.filter(
            status='ACTIVE'
        ).count(),

        'completed_projects': projects.filter(
            status='COMPLETED'
        ).count(),

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

        'upcoming_tasks': tasks.exclude(
            status='COMPLETED'
        ).order_by('due_date')[:5],
    }

    return render(
        request,
        'dashboard.html',
        context
    )