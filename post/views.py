from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
# Create your views here.
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from .models import BlogPost, Like
from .forms import BlogPostForm, PictureFormSet
from django.views.decorators.csrf import csrf_exempt

from django.db.models import Case, When, Value, BooleanField
from django.shortcuts import render


class postsView(View):
    def get(self, request):
        posts = BlogPost.objects.all()
        if request.user.is_authenticated:
            likes = Like.objects.filter(user=request.user)
        else:
            likes = None

        posts = BlogPost.objects.annotate(
            liked=Case(
                When(like__user=request.user, like__like=True, then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            ),
            disliked=Case(
                When(like__user=request.user, like__like=False, then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            ),
        ).prefetch_related('like_set')
        return render(request, 'posts.html', {'posts': posts, 'likes': likes})


class AddPost(View):
    def post(self, request):
        blog_post_form = BlogPostForm(request.POST)
        formset = PictureFormSet(request.POST, request.FILES, instance=blog_post_form.instance)
        if blog_post_form.is_valid() and formset.is_valid():
            blog_post = blog_post_form.save(commit=False)
            # Add or modify values here
            blog_post.create_by = request.user  # Example: setting the logged-in user
            blog_post.save()
            formset.post_id = blog_post
            formset.save()
            return redirect('home')

    def get(self, request):
        blog_post_form = BlogPostForm()
        formset = PictureFormSet(instance=BlogPost())
        return render(request, 'add_post.html', {
            'blog_post_form': blog_post_form,
            'formset': formset
        })


class postView(View):
    def get(self, request, slug):

        posts = BlogPost.objects.filter(slug=slug)
        if posts:
            return render(request, 'post.html', {'post': posts[0]})
        else:
            redirect('posts')


@csrf_exempt  # Only for testing; handle CSRF properly in production
@require_http_methods(["POST"])
def like_ajax_view(request):
    if request.user.is_authenticated:
        slug = request.POST.get('slug')
        type = request.POST.get('type')
        post = get_object_or_404(BlogPost, slug=slug)
        like = True if type == 'like' else False
        find_uniq = Like.objects.filter(user=request.user, post=post)

        if not find_uniq:

            Like.objects.update_or_create(
                post=post,
                user=request.user,
                like=like
            )
        else:
            find_uniq = find_uniq[0]
            like = None if (find_uniq.like == True and like == True) or (
                    find_uniq.like == False and like == False) else like
            Like.objects.update_or_create(
                post=post,
                user=request.user,
                defaults={'like': like}
            )
            print(like)
        return JsonResponse({'status': 'success', 'like': like, 'slug': slug})
    else:
        return JsonResponse({'status': 'error', 'message': 'User not authenticated'})
