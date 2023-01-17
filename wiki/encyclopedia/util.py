import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None


def HTML_convert(entry):


    HTML_entry = entry

    #Find "##" and convert to <h2>
    heading_pattern = re.compile(r'(\B##\s?)([A-Za-z]?\w*)')
    headings = heading_pattern.finditer(entry)
    for heading in headings:
        HTML_entry = HTML_entry.replace(f"{heading.group()}", f"<h2>{heading.group(2)}</h2>")
        
    #Find "#" and convert to <h1>
    heading_pattern = re.compile(r'(\B#\s?)([A-Za-z]?\w*)')
    headings = heading_pattern.finditer(HTML_entry)
    for heading in headings:
        HTML_entry = HTML_entry.replace(f"{heading.group()}", f"<h1>{heading.group(2)}</h1>")
    
    #Find links and convert to HTML <a>
    link_pattern = re.compile(r'(\B\[)([A-Za-z]?\w*)(\])(\()(.?\w*)(/.?\w*)(/)([A-Za-z]?\w*)(\))') 
    links = link_pattern.finditer(HTML_entry)
    for link in links:
        HTML_entry = HTML_entry.replace(f"{link.group()}", f"<a href='/encyclopedia/{link.group(8)}'>{link.group(8)}</a>")
    
    #Find bold text and convert to HTML <b>
    bold_pattern = re.compile(r'(\*{2})(.*?)(\*{2})') # ([\*\*])
    bolded = bold_pattern.finditer(HTML_entry)
    for bold in bolded:
        HTML_entry = HTML_entry.replace(f"{bold.group()}", f"<b>{bold.group(2)}</b>")

    #Find untitled list and convert to HTML <ul>
    list_pattern = re.compile(r'(\*\s?)([\w\s!]*)') # ([\*\*])
    list = list_pattern.finditer(HTML_entry)
    for item in list:
        HTML_entry = HTML_entry.replace(f"{item.group()}", f"<li>{item.group(2)}</li>")
        #print(item.group())

    #Find paragraph and convert to HTML <p>
    
    
    blankline_pattern = re.compile(r'^\#')
    blanklines = blankline_pattern.finditer(HTML_entry)
    for blankline in blanklines:
        
        HTML_entry = HTML_entry.replace(f"{blankline.group()}", f"blank{blankline.group()}")
        print(blankline)
    #paragraph_pattern = re.compile(r'(.+?\n\n|.+?$)') # ([\*\*])
    #paragraphs = paragraph_pattern.finditer(entry)
    #for paragraph in paragraphs:
        #HTML_entry = HTML_entry.replace(f"{paragraph.group()}", f"<p>{paragraph.group()}</p>")
        #print(paragraph.group())


     
    return HTML_entry








