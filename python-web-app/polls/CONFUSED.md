Going through the documentation on forms, I'm getting `Server Error (500)` and I don't know why. First I wrote some really basic code that works, and then I made a slight mod and it stopped working.

All the code described below is [on Github](https://github.com/JeffreyBenjaminBrown/learning-aws/tree/forms/python-web-app). Below I've stripped the comments from it.

# The working code

Here are some working views, in `polls/views.py`. `silly_form` gets someone's name, and hands it off to `silly_form_process`, which changes the name slightly without rendering anything, and then hands it off to `silly_form_result`, which displays some text including the name.

```python
def silly_form ( request ) :
    return render (
        request,
        "polls/silly-form.html",
        { 'default_name' : "Replace this text with your name, please." } )

def silly_form_process ( request ):
  your_name = request . POST [ 'your_name' ]
  return HttpResponseRedirect (
    reverse( 'polls:silly-form-result',
             kwargs = { "name_augmented" : "Mr. " + your_name } ) )

def silly_form_result ( request, name_augmented ):
  return render (
      request,
      "polls/silly-form-result.html",
      { 'name_augmented' : name_augmented } )
```

Here are the templates in `polls/templates/polls/` used by the above views. They work:
```html
# silly-form.html
<form action="{% url 'polls:silly-form-process'%}" method="post">
    {% csrf_token %}
    <label for="What's your name?">Your name: </label>
    <input id="your_name"
           type="text"
           name="your_name"
           value="{{ default_name }}">
    <input type="submit" value="OK">
</form>

# silly-form-result.html
Hello, {{ name_augmented }}.
```

Last, here is my working code in `urls.py`.
```python
# urls.py
  path( 'silly-form/',
        views.silly_form,
        name='silly-form' ),

  path( 'silly-form-process/',
        views.silly_form_process,
        name='silly-form-process' ),

  path( 'silly-form-result/<name_augmented>/',
        views.silly_form_result,
        name='silly-form-result' ),
```


# The broken code

The view and template below are based the Django documentation page called [Creating forms from models](https://docs.djangoproject.com/en/3.1/topics/forms/modelforms/).  The changes to `urls.py` is something I made up, lacking any model to mimic.

I added this view in `views.py`:
```python
# views.py
def silly_form_2 ( request ):
  if request . method == 'POST':
    form = NameForm ( request . POST )
    if form . is_valid ():
      return HttpResponseRedirect (
        reverse(
          'polls:silly-form-result',
          kwargs = { "name_augmented" :
                   "Mr. " + form . cleaned_data . your_name } ) )
  else: form = NameForm()
  return render ( request,
                  'silly-form-2.html',
                  { 'form' :  form } )
```

That uses a new class I had to define in `forms.py`:
```python
class NameForm ( forms. Form ):
  your_name = forms.CharField(
      label = 'Your name',
      max_length = 100 )
```

I added this template at `polls/templates/polls/silly-form-2.html`:
```html
<form action = "{% url 'polls:silly-form-2'%}"
      method = "post">
    {% csrf_token %}
    {{ form }}
    <input type="submit" value="Submit">
</form>
```

I added this to `urls.py`:
```python
  path( 'silly-form-2/',
        views.silly_form_2,
        name='silly-form-2' ),
```

When I visit `http://localhost:8000/myapp/polls/silly-form/` (the earlier code), it works, but when I visit `http://localhost:8000/myapp/polls/silly-form-2/` all I see is `Server Error (500)`.


# The only error message I can find

I believe the only Apache error logs to view are in `/var/log/apache2/`. There I find three files: `access.log  error.log  other_vhosts_access.log`. Tje forst os empty, and the second shows nothing it doesn't show when things are working normally. The third shows this:

```
127.0.0.1:80 172.17.0.1 - - [31/Oct/2020:01:48:23 +0000] "GET /myapp/polls/silly-form-2/ HTTP/1.1" 500 417 "-" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"
127.0.0.1:80 172.17.0.1 - - [31/Oct/2020:01:48:23 +0000] "GET /favicon.ico HTTP/1.1" 404 490 "http://localhost:8000/myapp/polls/silly-form-2/" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"
```
