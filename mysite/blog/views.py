from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = "blog/post/list.html"


def post_list(request):
    object_list = Post.published.all()
    # 3 post per page
    paginator = Paginator(object_list, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an Integer
        # download first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is higher than the number of the last page of results
        # than the last page is downloaded
        posts = paginator.page(paginator.num_pages)

    return render(request,
                  "blog/post/list.html",
                  {"page": page,
                   "posts": posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status="published",
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request,
                  "blog/post/detail.html",
                  {"post": post})


def post_share(request, post_id):
    # Pobranie posta na podstawie jego identyfikatora
    post = get_object_or_404(Post, id=post_id, status="published")

    if request.metod == "POST":
        # Formularz został wysłany
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Weryfikacja pól formularza zakończyła się powodzeniem
            cd = form.cleaded_data
            # więc można wysłać wiadomość e-mail
    else:
        form = EmailPostForm()
        return render(request, "blog/post/share.html", {"post": post, "form": form})
