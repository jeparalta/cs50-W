from django.shortcuts import render
from django.http import HttpResponse
from django import forms
import random

from . import util

class QueryForm(forms.Form):

    query = forms.CharField(label="Search")

class EntryForm(forms.Form):
    
    title = forms.CharField(label="Title")
    description = forms.CharField(widget=forms.Textarea(attrs={"rows":"5"}))





def index(request):

    if request.method == "POST":
        form = QueryForm(request.POST)

        if form.is_valid():
            query = form.cleaned_data["query"].lower()
            entries = util.list_entries()
            matches = []
            for entry in entries:
                if entry.lower() == query:
                    match = util.get_entry(query)
                    return render(request, "encyclopedia/entry.html", {
                        "title": entry, "entry": match
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

    html = util.HTML_convert(entry)

    #print(html)

    if entry == None:
        return render(request, "encyclopedia/apology.html", {
            "title": title
        })
    else:    
        return render(request, "encyclopedia/entry.html", { 
            "title": title, "entry": html
    })

def newpage(request):

    if request.method == "POST":
        form = EntryForm(request.POST)

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
        # Create new entry file
        f = open(f"entries/{title}.md", "x")
        f.write(f"{description}")
        f.close()


        entry = util.get_entry(title)
        # Convert to HTML
        html = util.HTML_convert(entry)
        

        if entry == None:
            return render(request, "encyclopedia/apology.html", {
                "title": title
            })
        else:    
            return render(request, "encyclopedia/entry.html", { 
            "title": title, "entry": html
        })

    return render(request, "encyclopedia/newpage.html", {
        "newpageform": EntryForm()
    })

def edit(request):

    if request.method == "POST":

        # Display pre-populated form to edit existing entry
        title = request.POST["title"]
        description = util.get_entry(title)
        #description = request.POST["entry"] This option gets the html version
        
        editform = EntryForm(initial={'title': f'{title}', 'description': f'{description}'})
        return render(request, "encyclopedia/edit.html", {
            "title": title, "entry": entry, "editform": editform
        })

def update(request):

    if request.method == "POST":

        # Get updated info from edited form
        form = EntryForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            

        
        # Update existing entry from edited form
        f = open(f"entries/{title}.md", "w")
        f.write(f"{description}")
        f.close()

        # Convert to HTML
        html = util.HTML_convert(description)
        

        return render(request, "encyclopedia/entry.html", { 
        "title": title, "entry": html
        })

def randomchoice(request):

    # List all entries
    entries = util.list_entries()
    # Choose 1 random entry
    randomchoice = random.choice(entries)
    # get entry description
    entry = util.get_entry(randomchoice)
    # Convert to HTML
    html = util.HTML_convert(entry)
        
    # Check if entry exists, if not return error msg
    if entry == None:
        return render(request, "encyclopedia/apology.html", {
                "title": randomchoice
        })
    # If entry exists display entry page
    else:    
        return render(request, "encyclopedia/entry.html", { 
            "title": randomchoice, "entry": html
        })

    

   






    

    





