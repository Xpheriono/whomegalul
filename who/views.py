import logging

from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import generic
from django.contrib import messages

from .models import UserInfo
from .services import TwitchAPI

logger = logging.getLogger('django')

# Landing page
class IndexView(generic.TemplateView):
    template_name = 'who/index.html'

# Search results page
class ResultsView(generic.DetailView):
    template_name = 'who/results.html'
    model = UserInfo
    pk_url_kwarg = 'login'
    context_object_name = 'userinfo'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

# Manage the form submit request
def verify_query(request):
    q = request.GET.get('q').strip().lower() # query from search-box
    try:
        q_user = UserInfo.objects.get(login=q)
        return HttpResponseRedirect(reverse('results', kwargs={'login': q}))
    except UserInfo.DoesNotExist as error:
        twitch = TwitchAPI()
        q_user = twitch.get_user(q).json()
        if q_user and 'data' in q_user and q_user['data']:
            UserInfo.objects.create(info=q_user, login=q)
            return HttpResponseRedirect(reverse('results', kwargs={'login': q}))
        else:
            messages.error(request, 'Unable to retrieve any results for {}'.format(q))
            return redirect('index')
    