from django.views.generic import View
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from forms import CreateTaskForm, UpdateTaskForm, AuthenticatedCommentForm, AnonymousCommentForm
from models import Task, Comment
from datetime import datetime


class AllTasksListView(View):
    def get(self, request):
        tasks = Task.objects.all().order_by('created')

        return render(request, 'all-tasks-list.html', {
            'tasks': tasks,
        })

alltasks = AllTasksListView.as_view()


class UserTasksListView(View):
    def get(self, request, *args, **kwargs):
        username = kwargs.get('username')
        list_owner = get_object_or_404(User, username=username)
        tasks = Task.objects.filter(creator=list_owner).order_by('created')

        return render(request, 'user-tasks-list.html', {
            'list_owner_username': list_owner.username,
            'tasks': tasks,
        })

usertasks = UserTasksListView.as_view()


class TaskDetailView(View):
    def get(self, request, *args, **kwargs):
        year = kwargs.get('year')
        month = kwargs.get('month')
        day = kwargs.get('day')
        slug = kwargs.get('slug')
        task = get_object_or_404(Task, created__year=year, created__month=month, created__day=day, slug=slug)
        comments = Comment.objects.filter(task_id=task.id).order_by('-created')

        context = {
            'task': task,
            'comments': comments,
        }

        if task.allow_comments:
            if request.user.is_authenticated():
                comment_form = AuthenticatedCommentForm()
            else:
                comment_form = AnonymousCommentForm()

            context['comment_form'] = comment_form

        return render(request, 'task-detail.html', context)

    def post(self, request, *args, **kwargs):
        year = kwargs.get('year')
        month = kwargs.get('month')
        day = kwargs.get('day')
        slug = kwargs.get('slug')
        task_id = request.POST.get('task_id')
        task = get_object_or_404(Task, pk=task_id)

        if request.user.is_authenticated():
            comment_form = AuthenticatedCommentForm(request.POST)

            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.task_id = task_id
                new_comment.user_id = request.user.id
                new_comment.created = datetime.now()
                new_comment.save()
                task.comment_count += 1
                task.save()

                messages.info(request, "Your comment has been added")
                return HttpResponseRedirect(reverse('taskdetail', args=[year, month, day, slug]))

            messages.error(request, "Error: invalid form")

        else:
            comment_form = AnonymousCommentForm(request.POST)

            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.task_id = task_id
                new_comment.created = datetime.now()
                new_comment.save()
                task.comment_count += 1
                task.save()

                messages.info(request, "Your comment has been added")
                return HttpResponseRedirect(reverse('taskdetail', args=[year, month, day, slug]))

            messages.error(request, "Error: invalid form")

        return render(request, 'task-detail.html', {
            'task': task,
            'comment_form': comment_form,
        })

taskdetail = TaskDetailView.as_view()


class CreateTaskView(View):
    def get(self, request):
        if request.user.is_authenticated():
            form = CreateTaskForm()

            return render(request, 'create-task.html', {
                'form': form,
            })
        return HttpResponseRedirect(reverse('login'))

    def post(self, request, *args, **kwargs):
        form = CreateTaskForm(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.creator = request.user
            new_task.created = datetime.now()
            new_task.progress = 0
            new_task.comment_count = 0
            new_task.save()

            messages.info(request, "Your task has been added")
            return HttpResponseRedirect(reverse('taskdetail', args=[new_task.created.year, new_task.created.month, new_task.created.day, new_task.slug]))

        return render(request, 'create-task.html', {
            'form': form,
        })

createtask = CreateTaskView.as_view()


class UpdateTaskView(View):
    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('task_id')
        task = get_object_or_404(Task, pk=task_id)
        form = UpdateTaskForm(instance=task)

        return render(request, 'update-task.html', {
            'form': form,
            'task': task,
        })

    def post(self, request, *args, **kwargs):
        task_id = kwargs.get('task_id')
        task = get_object_or_404(Task, pk=task_id)
        form = UpdateTaskForm(request.POST, instance=task)

        if form.is_valid():
            updated_task = form.save(commit=False)
            updated_task.updated = datetime.now()
            updated_task.save()
            messages.info(request, "The task has been updated")
            return HttpResponseRedirect(reverse('taskdetail', args=[updated_task.created.year, updated_task.created.month, updated_task.created.day, updated_task.slug]))
        messages.error(request, "Error: invalid form")

        return render(request, 'update-task.html', {
            'form': form,
        })

updatetask = UpdateTaskView.as_view()
