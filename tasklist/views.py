# Create your views here.
from django.shortcuts import render_to_response
from django.template import Context, RequestContext
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
import datetime

from tasklist.forms import *




def homepage(request):
  if request.user.is_authenticated():
    user = request.user
    tasklist = user.userprofile.current_list
    if not tasklist:
      try:
        tasklist = user.tasklists.all()[0]
      except:
        form = TasklistForm()
        return render_to_response(
          'list/error_no_lists.html', { 'form':form, },
          context_instance=RequestContext(request)
        )
        
    return HttpResponseRedirect('/list/' + str(tasklist.id))



  else:
    return render_to_response('global/homepage.html', context_instance=RequestContext(request))



@login_required
def list_page(request, list_id):
  tasklist = Tasklist.objects.get(id=list_id)

  if tasklist.user != request.user:
    return HttpResponseForbidden("You can't see that list. It's not yours, how rude.")
  else:

    tasks = tasklist.listitem_set.exclude(complete = True).exclude(deleted = True)
    completed_tasks = tasklist.listitem_set.filter(complete = True).exclude(deleted = True)

    # set this list as the default unless it's already set
    if request.user.userprofile.current_list != tasklist:
      request.user.userprofile.current_list = tasklist
      request.user.userprofile.save()
      message = "Your new default tasklist is " + tasklist.title
      messages.add_message(request, messages.INFO, message)

    # set up or handle the task adding form
    if request.method == 'POST':
      form = ListitemForm(request.POST)
      if form.is_valid():
        task = form.save(commit=False)
        task.tasklist_id = list_id
        task = form.save()
        message = "Task added!"
        messages.add_message(request, messages.SUCCESS, message)
        return HttpResponseRedirect('/list/' + list_id)
    else:
      form = ListitemForm()

    return render_to_response(
      'list/list_page.html', 
      { 
        'tasklist':tasklist,
        'tasks':tasks,
        'completed_tasks':completed_tasks,
        'form':form
      },
      context_instance=RequestContext(request)
    )


@login_required
def new_list(request):
  if request.method == 'POST':
    form = TasklistForm(request.POST)
    if form.is_valid():
      tasklist = form.save(commit=False)
      tasklist.user = request.user
      tasklist = form.save()
      message = "Sweet! You've created a new list!"
      messages.add_message(request, messages.SUCCESS, message)
      return HttpResponseRedirect('/list/' + str(tasklist.id))
  else:
    form = TasklistForm()

  return render_to_response(
    "global/modelform.html",
    { 'form' : form, }, 
    context_instance=RequestContext(request)
  )


@login_required
def delete_list(request, list_id):
  tasklist = Tasklist.objects.get(id = list_id)
    
  if tasklist.user != request.user:
    return HttpResponseForbidden("You can't delete that list. It's not yours, how rude.")

  if tasklist.user.tasklists.count() < 2:
    message = "You can't delete your final list."
    messages.add_message(request, messages.ERROR, message)
    return HttpResponseRedirect('/')
  else:
    tasklist.user.userprofile.current_list = None
    tasklist.user.userprofile.save()
    tasklist.user = None
    tasklist.delete()
    return HttpResponseRedirect('/')




@login_required
def add_task(request, list_id):
  tasklist = Tasklist.objects.get(id = list_id)
  
  if tasklist.user != request.user:
    return HttpResponseForbidden("You can't add to that list. It's not yours, how rude.")

  if request.method == 'POST':
    form = ListitemForm(request.POST)
    if form.is_valid():
      task = form.save(commit=False)
      task.tasklist_id = list_id
      task = form.save()
      message = "Task added!"
      messages.add_message(request, messages.SUCCESS, message)
      return HttpResponseRedirect('/list/' + list_id)
  else:
    form = ListitemForm()

  return render_to_response(
  "global/modelform.html",
    { 'form' : form, }, 
    context_instance=RequestContext(request)
  )




@login_required
def complete_task(request, task_id):
  task = Listitem.objects.get(id = task_id)
  
  if task.tasklist.user != request.user:
    return HttpResponseForbidden("You can't complete that task. It's not yours, how rude.")

  task.complete = True
  task.completed_on = datetime.datetime.now()
  task.save()
  message = 'Task completed! <a href="/uncomplete_task/' + str(task.id) + '" class="undo_link">undo</a>'
  messages.add_message(request, messages.SUCCESS, message)
  return HttpResponseRedirect("/list/" + str(task.tasklist.id))




@login_required
def uncomplete_task(request, task_id):
  task = Listitem.objects.get(id = task_id)
  
  if task.tasklist.user != request.user:
    return HttpResponseForbidden("You can't un-complete that task. It's not yours, how rude.")

  task.complete = False
  task.completed_on = None
  task.added_on = datetime.datetime.now()
  task.save()
  message = "Task un-completed!"
  messages.add_message(request, messages.SUCCESS, message)
  return HttpResponseRedirect("/list/" + str(task.tasklist.id))




@login_required
def delete_task(request, task_id):
  task = Listitem.objects.get(id = task_id)
  
  if task.tasklist.user != request.user:
    return HttpResponseForbidden("You can't delete that task. It's not yours, how rude.")

  tasklist_id = task.tasklist.id
  task.deleted = True
  task.deleted_on = datetime.datetime.now()
  task.save()
  message = 'Task deleted! <a href="/undelete_task/' + str(task.id) + '" class="undo_link">undo</a>'
  messages.add_message(request, messages.SUCCESS, message)
  return HttpResponseRedirect("/list/" + str(tasklist_id))




@login_required
def undelete_task(request, task_id):
  task = Listitem.objects.get(id = task_id)
  
  if task.tasklist.user != request.user:
    return HttpResponseForbidden("You can't un-delete that task. It's not yours, how rude.")

  tasklist_id = task.tasklist.id
  task.deleted = False
  task.deleted_on = None
  task.save()
  message = "Task resurrected!"
  messages.add_message(request, messages.SUCCESS, message)
  return HttpResponseRedirect("/list/" + str(tasklist_id))




@login_required
def logout_page(request):
    logout(request) 
    return HttpResponseRedirect('/')




import datetime
def signup(request):
    if request.method == 'POST':
        unique_user_name = datetime.datetime.now().strftime('%y%m%d%H%M%S%f')
        data = {
            "email": request.POST['email'],
            "username": unique_user_name,
            "password1": request.POST['password1'],
            "password2": request.POST['password1'],
            #"slug": slugify(request.POST['display_name']),
            }

        form = SignUpForm(data)

        if User.objects.filter(email = request.POST['email']):
            message = "That email address is already in use. You might want to just reset your password."
            messages.add_message(request, messages.ERROR, message)

        if form.is_valid():
            user = form.save()
            up = UserProfile()
            up.user_id = user.id
            up.save()
            password = request.POST['password1']
            nu_user = authenticate(email=user.email, password=password)
            if nu_user is not None:
                if nu_user.is_active:
                    login(request, nu_user)
            
            return HttpResponseRedirect("/")
            

        else:
            message = "There was a problem! Please review the form below and correct any errors."
            messages.add_message(request, messages.ERROR, message)

    else:
        form = SignUpForm()

    return render_to_response(
        'registration/signup.html',
        { 
            'form':form, 
            'title': "Register for an account"
        }, 
        context_instance=RequestContext(request)
    )

