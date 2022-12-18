import os, sys, json, re
from jinja2 import Environment, BaseLoader
from pathlib import Path
import datetime

print("STATUS : Script started")

## Load database from JSON file

with open('db.json', encoding="utf-8") as f:
    database = json.load(f)

    
## Load template from file

with open("index.html", encoding="utf-8") as f:
    template_full = f.read()
header = template_full.split("<main>")[0]
footer = template_full.split("</main>")[1]

## Generate pages

page_input = {
    "research" : {
        "publications" : database["publishedPapers"],
        "working_projects" : database["workingPapers"],
    },
    "code_and_data" : {
        "projects" : database["projects"],
    },
    "talks_and_classes" : {
        "talks" : database["talks"],
        "classes" : database["teaching"], 
    },
    "blog_posts" : {
        "articles" : database["articles"],
    }
}

for label, data in page_input.items():
    with open(Path.cwd() / 'templates' / f'{label}.html', encoding="utf-8") as f:
        template_html = f.read()

    template_html = header + template_html + footer

    template = Environment(loader=BaseLoader()).from_string(template_html)

    render = template.render(data)

    with open(Path.cwd() / f"{label}.html", encoding = "utf-8", mode = "w") as f:
        f.write(render)

print("STATUS : Pages generated")

## Generate resume

with open(Path.cwd() / 'templates' / 'resume.html', encoding="utf-8") as f:
    template_html = f.read()

template = Environment(loader=BaseLoader()).from_string(template_html)

render = template.render({
    "resume" : database,
    "date" : datetime.datetime.now().strftime("%B %d, %Y")
    })

with open(Path.cwd() / 'resume.html', encoding = "utf-8", mode = "w") as f:
    f.write(render)

print("STATUS : Resume generated")

print("STATUS : Script finished!")