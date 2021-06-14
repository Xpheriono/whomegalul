import logging

from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.forms.models import model_to_dict

from .models import UserInfo
from .forms import SearchForm

logger = logging.getLogger(__name__)

# Landing page
class IndexView(generic.TemplateView):
    template_name = 'who/index.html'

# Search results page
class ResultsView(generic.DetailView):
    template_name = 'who/results.html'
    model = UserInfo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        login_match = kwargs.get('login')
        context['users'] = UserInfo.objects.filter(login__iexact=login_match)
        #context['users'] = []
        logger.info('the context is {} \t the login_match is {}'.format(context['users'], login_match))
        return context

# Manage the form submit request
class SubmitView(generic.edit.CreateView):
    model = UserInfo

    # get the request
    def get(self, request):
        q = request.GET.get('q')
        # if query exists then redirect to it, otherwise process failure
        try:
            user = UserInfo.objects.get(login__iexact=q)
            logger.info('user is {} and login is {}'.format(user, user.login))
            return HttpResponseRedirect(reverse('results', kwargs={'login': user.login}))
        except UserInfo.DoesNotExist:
            user = None
            return HttpResponseRedirect(reverse('index', kwargs={}))
            