from django.shortcuts import render
from django.http import HttpResponse

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    
    entry = util.get_entry(title)

    if entry == None:
        return render(request, "encyclopedia/apology.html", {
            "title": title
        })
    else:    
        return render(request, "encyclopedia/entry.html", { 
        "title": title, "entry": entry
    })




