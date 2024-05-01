from django.urls import path
from . import views

urlpatterns = [
    path("",views.StartingPageView.as_view(), name="starting-page"),
    path("projects", views.AllProjectsView.as_view(), name="projects-page"),
    path("projects/<slug:slug>", views.SingleProjectView.as_view(), name="project-detail-page"), #/projects/my-first-post
    path("read-later", views.ReadLaterView.as_view(), name="read-later")
]