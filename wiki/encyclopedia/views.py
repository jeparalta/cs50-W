from django.shortcuts import render
from django.http import HttpResponse
from django import forms

from . import util

class QueryForm(forms.Form):

    query = forms.CharField(label="Search")

class NewPageForm(forms.Form):
    
    title = forms.CharField(label="Title")
    description = forms.CharField(widget=forms.Textarea(attrs={"rows":"5"}))


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
            if not matches:
                return render(request, "encyclopedia/apology.html", {
            "title": "An entry for this search"
        })
            
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

    if request.method == "POST":
        form = NewPageForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
        # Check if an entry with this title exists
        entries = util.list_entries()
        for entry in entries:
            if entry.lower() == title.lower():
                return render(request, "encyclopedia/apology2.html", {
                    "msg": "An entry with this name already exists!"
                })

    
    return render(request, "encyclopedia/newpage.html", {
        "newpageform": NewPageForm()
    })






