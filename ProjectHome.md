![http://panos.solhost.org/temp/sleepy.png](http://panos.solhost.org/temp/sleepy.png)

## What is Sleepy? ##
Sleepy, allows you to create a static site by rendering Django templates to HTML.

## Why? ##
This allows for, easy prototyping and easier creation of static websites, where the whole workhorse of Django is not needed.

You are allowed to use **all** of Django's builtin tags and filters.

If you want more, you can always move to the actual Django, since the templates are totally compatible.

## How? ##
You can start a new project by typing:
```
sleepy.py --startproject=myfunsite
```

Add your templates in there, when you're ready you can _compile_ them by doing:
```
sleepy.py --make
```

And voila!