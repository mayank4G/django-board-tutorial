from urllib import response
from django.shortcuts import redirect, render, get_object_or_404

# Create your views here.
from django.http import Http404, HttpResponse

from boards.forms import NewTopicForm, PostForm
from .models import Board, Topic, Post
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import logging

def user_profile(request):
    try:
        if request.user.username in User:
            return render(request, "profile.html", {'username': request.user.username})
        
    except:
        return redirect("signup")



def topics_post(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    return render(request, 'topic_posts.html', { 'topic': topic })

@login_required
def reply_topic(request, pk, topic_pk):
    logging.debug("pk" + str(pk))
    logging.debug("topicpk" + str(topic_pk))
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('topics_post', pk=pk, topic_pk=topic_pk)
    else:
        form = PostForm()
    return render(request, 'reply_topic.html', {'topic' : topic, 'form': form})



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

@login_required
def new_topic(request, pk):
    
    board = get_object_or_404(Board,pk=pk)
    
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()
            Post.objects.create(
                message = form.cleaned_data.get('message'),
                topic = topic,
                created_by = request.user
            )
            
            return redirect('board_topics', pk=board.pk)
    else:   
        form = NewTopicForm()
    
    return render(request, 'new_topic.html', {'board' : board, 'form' : form} )