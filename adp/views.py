from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.template import loader
from ferrp.adp.utils import get_adp_yearly_analysis


def adp_analysis_index(request, template=loader.get_template('index_adp.html')):
    return HttpResponse(template.render({}, request))

def adp_yearly_analysis(request):
    data = get_adp_yearly_analysis()
    return HttpResponse(data)
