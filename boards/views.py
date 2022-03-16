from urllib import response
from django.shortcuts import redirect, render, get_object_or_404

# Create your views here.
from django.http import Http404, HttpResponse

from boards.forms import NewTopicForm
from .models import Board, Topic, Post
from django.contrib.auth.models import User


def user_profile(request):
    try:
        if request.user.username in User:
            return render(request, "profile.html", {'username': request.user.username})
        
    except:
        return redirect("signup")


def home(request):
    boards = Board.objects.all()
    # boards_details = {}
    
    # for board in boards:
    #     boards_details['name'] = board.name
    #     boards_details['description'] = board.description
        
    context = { 'boards': boards }
    # user = get_object_or_404(User)
    
    return render(request, 'home.html', context)


def board_topics(request, pk):
    
    board = get_object_or_404(Board,pk=pk)
    
    context = {'board' : board }
    
    return render(request, 'topics.html', context)


def new_topic(request, pk):
    
    board = get_object_or_404(Board,pk=pk)
    
    if request.method == 'POST':
        # subject = request.POST['subject']
        # message = request.POST['message']
        
        # user = User.objects.first()

        # topic = Topic.objects.create(
        #     subject = subject,
        #     board = board,
        #     starter = user
        # )
        # topic.save()

        # post = Post.objects.create(
        #     message = message,
        #     topic = topic,
        #     created_by = user
        # )
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save()
            return redirect('board_topics', pk=board.pk)
    
    else:   
        form = NewTopicForm()
    
    return render(request, 'new_topic.html', {'board' : board, 'form' : form} )