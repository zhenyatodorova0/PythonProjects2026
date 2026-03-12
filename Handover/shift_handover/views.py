from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from shift_handover.forms import Searchform, PostForm
from shift_handover.models import Post


# Create your views here.

def index(request: HttpRequest) -> HttpResponse:
    return HttpResponse("Hello world")

def dashboard(request: HttpRequest) -> HttpResponse:
    form = Searchform(request.GET or None)
    posts = Post.objects.all()

    if request.method == "GET":
        if form.is_valid():
            query = form.cleaned_data["query"]
            posts = Post.objects.filter(title__icontains=query)

    context = {
        "posts": posts,
        "form": form
    }

    return render(request, "dashboard.html", context)

def add_post(request: HttpRequest) -> HttpResponse:
    form = PostForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            post = Post(
                title=form.cleaned_data["title"],
                content=form.cleaned_data["content"],
                author=form.cleaned_data["author"],
                language=form.cleaned_data["language"],
            )
            post.save()
            return redirect('dashboard')
    context = {
        "form": form
    }
    return render(request, "add-post.html", context)

# def landing_page(request: HttpRequest) -> HttpResponse:
#     latest_topic = ShiftHandover.objects.order_by('-publishing_date').first()
#
#     context = {
#         'latest_topic': latest_topic,
#         'page_title': 'Home'
#     }
#
#     return render(request, 'shift_handover/landing_page.html', context)
