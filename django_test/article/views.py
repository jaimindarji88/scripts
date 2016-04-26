from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from django.views.generic.base import TemplateView

# Create your views here.

def hello(request):
	name = 'Jack'
	html = '<html><body>My name {name}, Hello World</body></html>'.format(name=name)
	return HttpResponse(html)

def hello_template(request):
	name = 'Jaimin Darji'
	t = get_template('index.html')
	html = t.render(Context({'name': name}))
	return HttpResponse(html)

class HelloTemplate(TemplateView):

	template_name = 'index.html'

	def get_context_data(self, **kwargs):
		context = super(HelloTemplate, self).get_context_data(**kwargs)
		context['name'] = 'Jaimin'

		return context
