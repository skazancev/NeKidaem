from django.contrib.auth.models import User
from django.http import JsonResponse, Http404
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, CreateView, View, TemplateView, DeleteView

from blog.decorators import authorized_only
from blog.forms import PostForm
from blog.models import Post, Subscription, PostRead


@method_decorator(authorized_only, name='dispatch')
class SubscribeView(View):

    def post(self, request):
        try:
            user_id = request.POST.get('pk')
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'error': 'Пользователя не существует'})

        sub, created = Subscription.objects.get_or_create(user=user)

        # если пользователь уже в подписках, то удаляем его оттуда, иначе добавляем
        if request.user in sub.subscribers.all():
            sub.subscribers.remove(request.user.id)
            subscribed = False
            PostRead.objects.filter(user_id=request.user.id, post__user_id=user_id).delete()
        else:
            sub.subscribers.add(request.user.id)
            subscribed = True
        sub.save()

        return JsonResponse({'status': 'ok', 'subscribed': subscribed})


class BlogView(DetailView):
    model = User
    template_name = 'blog/user.html'

    def get_context_data(self, **kwargs):
        context = super(BlogView, self).get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(user_id=self.object.id).prefetch_related('user')
        return context


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.user = self.request.user
        post.save()
        return redirect(reverse('blog:detail', args=(post.user_id, post.id)))


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        # 2 запроса для получения всех постов
        # Получение списка id пользователей на которых подписан
        # Получение всех постов с этими id
        subscription = list(self.request.user.subscription.values_list('user_id', flat=True))
        subscription.append(self.request.user.id)
        context['posts'] = Post.objects.filter(user_id__in=subscription).prefetch_related('user').distinct()
        return context


class PostReadView(View):
    def post(self, request):
        try:
            post = Post.objects.exclude(user_id=request.user.id).get(pk=request.POST.get('post_id'))
        except Post.DoesNotExist:
            return JsonResponse({'status': 'error', 'error': 'Пост не найден'})

        PostRead.objects.get_or_create(user=request.user, post=post)
        return JsonResponse({'status': 'ok'})


class PostDeleteView(DeleteView):
    model = Post

    def get_object(self, queryset=None):
        return get_object_or_404(Post, user_id=self.request.user.id, pk=self.kwargs.get('pk'))

    def get_success_url(self):
        return reverse('blog:home')