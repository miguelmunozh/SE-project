# GUI

This repository contains an app.py file which handles which html files are shown in the specified urls, and the templates folder with html files for each page/window of the web application. 

The templates folder also contains a layout.html file which contains a main layout that will be displayed in all of the html files extending layout.html. This is done in order to avoid code repetition.

in the layout.html there are some blocks that child html files can override. For example. 
```
{% block content %}
{% endblock %} 
```
which is a block called content. if in the child class there is some html code like this :
```
{% extend layout.html %}
{% block content %}
<h1>Title</h1>
{% endblock %}
```
then the child class extends everything from the layout.html file and overrides the content of the empty block with the code that the child class provides within the block with the same name

see TaskView.html which extends layout.html for an example

and see [example](https://flask.palletsprojects.com/en/1.1.x/patterns/templateinheritance/)
for a better explanation.
