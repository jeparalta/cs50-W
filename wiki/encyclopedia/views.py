from django.shortcuts import render
from django.http import HttpResponse
from django import forms

from . import util

class QueryForm(forms.Form):

    query = forms.CharField(label="Search")

class NewPageForm(forms.Form):
    
    title = forms.CharField(label="Title")
    description = forms.CharField(label="Description")


def index(request):

    if request.method == "POST":
        form = QueryForm(request.POST)

        if form.is_valid():
            query = form.cleaned_data["query"].lower()
        #print(query)
            entries = util.list_entries()
            matches = []
            for entry in entries:
                if entry.lower() == query:
                    match = util.get_entry(query)
                    return render(request, "encyclopedia/entry.html", {
                        "entry": match
                    })
                elif query in entry.lower():
                    
                    matches.append(entry)
            
            print(matches)
                    
            return render(request, "encyclopedia/results.html", {
                        "entries": matches
                        })
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(), "form": QueryForm()
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

def newpage(request):
    
    return render(request, "encyclopedia/newpage.html")






