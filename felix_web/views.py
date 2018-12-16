from django.views.generic import TemplateView, DetailView, ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from felix_web.models import Session, Turn, User
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
import json
from functools import wraps
from django.utils import timezone
from django.conf import settings
from django.http import HttpRequest, HttpResponse


DjangoUser = get_user_model()


def dummy_json(view_func):

    @wraps(view_func)
    @method_decorator(dummy_json)
    def wrapper_view_func(request, *args, **kwargs):

        # Add simple validation or your own validation rule
        if request.content_type == 'application/json':
            if request.body:
                # Decode data to a dict object
                request.json = json.loads(request.body)
            else:
                request.json = None
        return view_func(request, *args, **kwargs)
    return wrapper_view_func



class HomeView(TemplateView):
    template_name = 'felix_web/home.html'


class SessionKoView(LoginRequiredMixin, ListView):
    model = Session

    def get_queryset(self):
        return self.model.objects.exclude(success=True, resolved_by_human=True)


class SessionKoDetail(LoginRequiredMixin, DetailView):
    model = Session

    def get_context_data(self, **kwargs):
        context = super(SessionKoDetail, self).get_context_data(**kwargs)
        context['turns'] = Turn.objects.filter(session_id=self.object.id)
        return context


class SaveTurn(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(SaveTurn, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        nomad = self.get_or_create_nomad(request.POST)
        user = self.get_user(request.POST)
        sesion = self.get_or_create_session(request.POST, nomad)
        turn = Turn.objects.create(nomad=nomad,
                                   user=user,
                                   session=sesion,
                                   lat=request.POST['lat'],
                                   lon=request.POST['lon'],
                                   question=request.POST['question'],
                                   answer=request.POST['answer'],

                                   )
        return JsonResponse({'200': 'OK'})

    @staticmethod
    def get_or_create_nomad(data):
        try:
            return User.objects.get(phone=data['nomad'])
        except ObjectDoesNotExist:
            return User.objects.create(phone=data['nomad'])

    @staticmethod
    def get_user(data):
        try:
            return DjangoUser.objects.get(id=data['user'])
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_or_create_session(data, nomad):
        try:
            session = Session.objects.get(data['session'])
            if data.get('end'):
                session.end = timezone.now()
                session.save()
            return session

        except ObjectDoesNotExist:
            return Session.objects.create(
                id=data['session'],
                nomad=nomad,
            )
