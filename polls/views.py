from multiprocessing import context
from django.http import HttpResponse
from django.template import loader
from . import twitter_api


def index(request):

    template = loader.get_template("polls/index.html")
    context = {
        "loaded":True,
        "numbers": [1,2,3,4,5,6,7,8,9,0]
    }

    return HttpResponse(template.render(context,request))


def search(request):
    template = loader.get_template("polls/index.html")
    char = request.GET['query'][0]
    text = request.GET['query'][1:]
    if char=="@":
        print("[USERNAME]: ", text)
        twitter_api.getTweetsFromUser(text)
    else:
        twitter_api.getTweetsFromHashtag(text)

    context = {
        "search":True,
    }

    

    return HttpResponse(template.render(context,request))