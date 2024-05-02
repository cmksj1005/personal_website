from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView
from django.views import View

from .models import Project
from .forms import FeedbackForm

# Create your views here.

class StartingPageView(ListView):
  template_name = "blog/index.html"
  model = Project
  ordering = ["-date"]
  context_object_name = "projects"

  def get_queryset(self):
    queryset = super().get_queryset()
    data = queryset[:3]
    return data
  
class AllProjectsView(ListView):
  template_name = "blog/all-projects.html"
  model = Project
  ordering = ["-date"]
  context_object_name = "all_projects"

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
    feedback_password = request.POST.get('password', "")

    context = {
      "project": project,
      "project_tags": project.tags.all(),
      "feedback_form": FeedbackForm(),
      "feedbacks": project.feedbacks.all().order_by("-id"),
      "saved_for_later": self.is_stored_project(request, project.id),
      "has_feedback": len(project.feedbacks.all()),
      "edit_feedback": edit_feedback,
      "feedback_password": feedback_password
    }
    return render(request, "blog/project-detail.html", context)

  def post(self, request, slug):
    feedback_form = FeedbackForm(request.POST)
    project = Project.objects.get(slug=slug)
    edit_feedback = request.GET.get('feedback_edit', False)
    feedback_password = request.POST.get('password', "")

    print(feedback_password)
    print(type(feedback_password))
    print(project.feedbacks.all()[0].user_password)
    print(type(project.feedbacks.all()[0].user_password))
    # If user input password to edit his/her feedback
    if feedback_password is not "":
      # I removed "feedback_form": feedback_form in the context, because this line shows form_field error messages
      context = {
        "project": project,
        "project_tags": project.tags.all(),
        "feedbacks": project.feedbacks.all().order_by("-id"),
        "saved_for_later": self.is_stored_project(request, project.id),
        "has_feedback": len(project.feedbacks.all()),
        "edit_feedback": edit_feedback,
        "feedback_password": feedback_password
      }
      return render(request, "blog/project-detail.html", context)
    # If user input valid feedback form
    if feedback_form.is_valid():
      feedback = feedback_form.save(commit=False)
      feedback.project = project
      feedback.save()
      return HttpResponseRedirect(reverse("project-detail-page", args=[slug]))
    # If user input invalid feedback form, it returns context include invalid feedback form so that screen shows form_field error message.
    context = {
      "project": project,
      "project_tags": project.tags.all(),
      "feedback_form": feedback_form,
      "feedbacks": project.feedbacks.all().order_by("-id"),
      "saved_for_later": self.is_stored_project(request, project.id),
      "has_feedback": len(project.feedbacks.all()),
      "edit_feedback": edit_feedback,
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

    if stored_projects is None:
      stored_projects = []

    project_id = int(request.POST["project_id"])

    if project_id not in stored_projects:
      stored_projects.append(project_id)

    else:
      stored_projects.remove(project_id)

    request.session["stored_projects"] = stored_projects

    return HttpResponseRedirect("/read-later")
