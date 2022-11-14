from django.shortcuts import render
from .models import *

# Create your views here.
def home(request):
    popularTag=0
    popularTagCount=0
    for pt in Tag.objects.all():
        if len(Post.objects.filter(tags=Tag.objects.get(title=pt))) > popularTagCount:
            popularTag=pt
            popularTagCount=len(Post.objects.filter(tags=Tag.objects.get(title=pt)))
    return render(request,'home.html',{'posts':Post.objects.all(),
                            'site':SiteDescription.objects.all(),
                            'popularTag':popularTag,
                            'tags':Tag.objects.all()
                        })
                
def viewPost(request,post):
    getPost = Post.objects.get(title=post)
    try:
        relatedPosts = Post.objects.filter(tags=Tag.objects.get(title=(getPost.tags.all()[0].title))).exclude(title=getPost.title)
    except:
        relatedPosts = Post.objects.all()
    postPool = list(Post.objects.all())
    if postPool.index(getPost)==len(postPool)-1:
        nextPost=[]
    else:
        nextPost=postPool[postPool.index(getPost)+1]
    if postPool.index(getPost)==0:
        prevPost=[]
    else:
        prevPost=postPool[postPool.index(getPost)-1]
    return render(request,'post.html',{'post':getPost,
                    'site':SiteDescription.objects.all(),
                    'tags':Tag.objects.all(),
                    'authors':Author.objects.all(),
                    'relatedPosts': relatedPosts,
                    'nextPost':nextPost,
                    'prevPost':prevPost
                })

def tagPage(request,tag):
    popularTag=0
    popularTagCount=0
    for pt in Tag.objects.all():
        if len(Post.objects.filter(tags=Tag.objects.get(title=pt))) > popularTagCount:
            popularTag=pt
            popularTagCount=len(Post.objects.filter(tags=Tag.objects.get(title=tag)))
    try:
        posts = Post.objects.filter(tags=Tag.objects.get(title=tag))
    except:
        posts = []
    return render(request,'tag.html',{'site':SiteDescription.objects.all(),
                            'popularTag':popularTag,
                            'posts':posts,
                            'tag':tag,
                            'authors':Author.objects.all()
                        })

def authorPage(request,author):
    popularTag=0
    popularTagCount=0
    for pt in Tag.objects.all():
        if len(Post.objects.filter(tags=Tag.objects.get(title=pt))) > popularTagCount:
            popularTag=pt
            popularTagCount=len(Post.objects.filter(tags=Tag.objects.get(title=pt)))
    try:
        posts = Post.objects.filter(author=Author.objects.get(name=User.objects.get(email=author)))
    except:
        posts = []
    return render(request,'author.html',{'site':SiteDescription.objects.all(),
                                'posts':posts,
                                'popularTag':popularTag,
                                'author':author,
                                'authors':Author.objects.all()
                            })

