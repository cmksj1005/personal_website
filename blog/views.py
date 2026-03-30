from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView
from django.views import View

from .models import Project
from .models import Feedback
from .forms import FeedbackForm


# Create your views here.
class StartingPageView(ListView):
    template_name = "blog/index.html"
    model = Project
    context_object_name = "projects"

    def get_queryset(self):
        return Project.objects.order_by('-date', '-id')[:3]


class AllProjectsView(ListView):
    template_name = "blog/all-projects.html"
    model = Project
    context_object_name = "all_projects"

    def get_queryset(self):
        return Project.objects.order_by('-date', '-id')

class SingleProjectView(View):
  def is_stored_project(self, request, project_id):
    stored_projects = request.session.get("stored_projects")
    if stored_projects is not None:
      is_saved_for_later = project_id in stored_projects
    else:
      is_saved_for_later = False
    return is_saved_for_later

  def get(self, request, slug):
    project = Project.objects.get(slug=slug)
    edit_feedback = request.GET.get('feedback_edit', False)
    go_to_edit_button = request.GET.get('go_to_edit_button', False)
    edit_id = request.GET.get('edit_id', -1)

    context = {
      "project": project,
      "project_tags": project.tags.all(),
      "feedback_form": FeedbackForm(),
      "feedbacks": project.feedbacks.all().order_by("-id"),
      "saved_for_later": self.is_stored_project(request, project.id),
      "has_feedback": len(project.feedbacks.all()),
      "edit_feedback": edit_feedback,
      "go_to_edit_button": go_to_edit_button,
      "edit_id": int(edit_id)
    }
    return render(request, "blog/project-detail.html", context)

  def post(self, request, slug):
    feedback_form = FeedbackForm(request.POST)
    project = Project.objects.get(slug=slug)
    edit_feedback = request.GET.get('feedback_edit', False)
    feedback_password = request.POST.get('password', None)
    edited_feedback = request.POST.get('edited_feedback', None)
    feedback_id = request.POST.get('feedback_id', None)
    go_to_edit_button = request.POST.get('go_to_edit_button', False)
    edit_id = request.POST.get('edit_id', -1)

    # If user finished to edit the feedback and click enter button
    if edited_feedback:
      # Retrieve the feedback instance
      feedback = get_object_or_404(Feedback, id=feedback_id)
      # Update the feedback text
      feedback.text = edited_feedback
      feedback.save() # Save the changes to the database

      context = {
        "project": project,
        "project_tags": project.tags.all(),
        "feedback_form": FeedbackForm(),
        "feedbacks": project.feedbacks.all().order_by("-id"),
        "saved_for_later": self.is_stored_project(request, project.id),
        "has_feedback": len(project.feedbacks.all()),
        "edit_feedback": edit_feedback,
        "feedback_password": feedback_password,
        "go_to_edit_button": go_to_edit_button,
        "edit_id": int(edit_id)
      }
      return render(request, "blog/project-detail.html", context)
 
    # If user input password to edit his/her feedback
    if feedback_password:
      # I removed "feedback_form": feedback_form in the context, because this line shows form_field error messages
      context = {
        "project": project,
        "project_tags": project.tags.all(),
        "feedback_form": FeedbackForm(),
        "feedbacks": project.feedbacks.all().order_by("-id"),
        "saved_for_later": self.is_stored_project(request, project.id),
        "has_feedback": len(project.feedbacks.all()),
        "edit_feedback": edit_feedback,
        "feedback_password": feedback_password,
        "go_to_edit_button": go_to_edit_button,
        "edit_id": int(edit_id)
      }
      return render(request, "blog/project-detail.html", context)
    
    # If user input valid feedback form
    if feedback_form.is_valid():
      feedback = feedback_form.save(commit=False)
      feedback.project = project
      feedback.save()
      return HttpResponseRedirect(reverse("project-detail-page", args=[slug]))
    
    context = {
      "project": project,
      "project_tags": project.tags.all(),
      "feedback_form": FeedbackForm(), 
      "feedbacks": project.feedbacks.all().order_by("-id"),
      "saved_for_later": self.is_stored_project(request, project.id),
      "has_feedback": len(project.feedbacks.all()),
      "edit_feedback": edit_feedback,
      "go_to_edit_button": go_to_edit_button
    }
    return render(request, "blog/project-detail.html", context)
  
class ReadLaterView(View):
  def get(self, request):
    stored_projects = request.session.get("stored_projects")

    context = {}

    if stored_projects is None or len(stored_projects) == 0:
      context["projects"] = []
      context["has_projects"] = False
    else:
      projects = Project.objects.filter(id__in=stored_projects)
      context["projects"] = projects
      context["has_projects"] = True

    return render(request, "blog/stored-projects.html", context)

  def post(self, request):
    stored_projects = request.session.get("stored_projects")
    project_slug = request.POST.get('project_slug', "")

    if stored_projects is None:
      stored_projects = []

    project_id = int(request.POST["project_id"])

    if project_id not in stored_projects:
      stored_projects.append(project_id)

    else:
      stored_projects.remove(project_id)

    request.session["stored_projects"] = stored_projects

    return HttpResponseRedirect(reverse("project-detail-page", args=[project_slug]))
