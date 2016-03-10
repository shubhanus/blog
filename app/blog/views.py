from app.blog.serializers import UserSerializer
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.utils import timezone
from app.blog.models import Posts, Comments


# class IndexView(generic.ListView):
#     template_name = 'blog/index.html'
#     context_object_name = 'latest_posts'
#
#     def get_queryset(self):
#         p1 = Posts.objects.order_by('-post_date')[:5]
#         return p1

# def index(request):
#     if 'member_name' in request.session :
#         m_name = request.session['member_name']
#         latest_post_list = Posts.objects.order_by('-post_date')[:5]
#         user_name = m_name
#         context = {'latest_posts':latest_post_list, 'name':user_name}
#         return render(request, 'blog/index.html', context)
#     else:
#         return render(request, 'blog/index.html')

@login_required
def index(request):
    latest_post_list = Posts.objects.order_by('-post_date')[:5]
    context = {'latest_posts': latest_post_list, 'name': request.user}
    return render(request, 'blog/index.html', context)


# class CommentsView(generic.DetailView):
#     model = Posts
#     template_name = 'blog/login.html'

@login_required
def post_comment(request, post_id):
    post = get_object_or_404(Posts, pk=post_id)
    try:
        user = request.POST['uname']
        cmnt = request.POST['cmnt']
    except (KeyError, post.DoesNotExist):
        return render(request, 'blog/index.html', {'posts': post, 'error_message': "Post is not Exist.",})
    else:
        new_c = post.comments_set.create(user_name=user, comment=cmnt, comment_date=timezone.now())
        new_c.save()
        return HttpResponseRedirect(reverse('blog:index'))


def del_comment(request, cmnt_id):
    try:
        cmnt = get_object_or_404(Comments, pk=cmnt_id)
    except (KeyError, cmnt_id.DoesNotExist):
        return render(request, 'blog/index.html', {'error_message': "comment is not Exist.",})
    else:
        cmnt.delete()
        return HttpResponseRedirect(reverse('blog:index'))


# def login(request):
#     if 'member_name' in request.session :
#         return HttpResponseRedirect(reverse('blog:index'))
#     else:
#         return render(request, "blog/login.html")


def login(request):
    #print "hi"
    return render(request, 'blog/login.html')


def login_user(request):
    # print "1"
    context ={}
    if request.method == 'POST':
        # print "2"
        user_name= request.POST.get('uname', None)
        password = request.POST.get('pwd', None)
        # print user_name
        account = authenticate(username=user_name, password=password)

        if account is not None:
            auth_login(request, account)
            serialized = UserSerializer(account)
            # return Response(serialized.data, status=status.HTTP_200_OK)
            # print serialized.data
            # context['username'] = user_name
            return HttpResponseRedirect(reverse('blog:index'))
            # return render_to_response(reverse('blog:index'), context)
    else:
        # return Response({
        #     'status': 'Unauthorized',
        #     'message': 'This account does not available.'
        # }, status=status.HTTP_401_UNAUTHORIZED)
        return HttpResponse("Your username and password didn't match.")
        # return render(request, 'blog/login.html')


# def logout(request):
#     try:
#         del request.session['member_name']
#     except KeyError:
#         pass
#     return HttpResponse("you are logged out")
#
#
# def member(request):
#         if request.method != 'POST':
#             raise Http404('Only POST request is allowed')
#         try:
#             m = Register_login.objects.get(user_name=request.POST['uname'])
#             if m.password == request.POST['pwd']:
#                 request.session['member_name'] = m.user_name
#                 return HttpResponseRedirect(reverse('blog:index'))
#         except Register_login.DoesNotExist:
#             return HttpResponse("Your username and password didn't match.")
