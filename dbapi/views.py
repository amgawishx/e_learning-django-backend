from django.views.decorators.csrf import ensure_csrf_cookie, requires_csrf_token
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator as decorator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.db.models import Q
from rest_framework import authentication, permissions
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from functools import lru_cache
from .serializers import model_serializers
from .models import data_models

requirements = [ensure_csrf_cookie,
                requires_csrf_token, csrf_protect, login_required]  # (login_url="login")]

user_permissions = {
    'dbapi.Student':
        {'question': ['create', 'edit']},
    'dbapi.Tutor':
        {'answer': ['create', 'edit', 'delete'],
         'question': ['delete'],
         'topic': ['create', 'edit', 'delete'],
         'resource': ['create', 'edit', 'delete'],
         'announcement': ['create', 'edit', 'delete'],
         'subject': ['create', 'edit', 'delete']}
}


def HttpJsonResponse(code: int) -> JsonResponse:
    return JsonResponse({'status': code})


def modelCheck(model: str) -> bool:
    result = model in {'university', 'college', 'department'}
    return result


def permissionCheck(user: 'BaseModel', model: str, action: str) -> bool:
    if action in user_permissions[user._meta.label][model]:
        return True
    return False


def shipJson(payload: list) -> dict:
    return {'payload': payload, 'status': 200}


# @decorator(requirements, name='get')
# @decorator(requirements, name='post')
# @decorator(requirements, name='put')
# @decorator(requirements, name='delete')
class DBAPI(APIView):

    permission_classes = [permissions.AllowAny]

    @lru_cache(maxsize=256)
    def get(self, request: 'HttpRequest', model: str, key: str = None,
            value: str = None, action: str = 'single',
            xkey: str = None) -> JsonResponse:
        # if not request.is_ajax():
        # return HttpJsonResponse(404)
        if key == 'password' or xkey == 'password':
            return HttpJsonResponse(403)
        try:
            model_object = data_models[model]
            is_many = True
            if action == 'all':
                query = model_object.objects.all()
                if xkey:
                    payload = [{'pk': item.pk, xkey: getattr(
                        item, xkey)} for item in query]
                    return JsonResponse(shipJson(payload), safe=False)
            elif action == 'filtered':
                query = model_object.objects.filter(Q((key, value)))
                if xkey:
                    payload = [{'pk': item.pk, xkey: getattr(
                        item, xkey)} for item in query]
                    return JsonResponse(shipJson(payload), safe=False)
            elif action == 'single':
                query = model_object.objects.get(Q((key, value)))
                is_many = False
                if xkey:
                    payload = [{xkey: getattr(query, xkey)}]
                    return JsonResponse(shipJson(payload), safe=False)
            if not query:
                raise LookupError
            payload = model_serializers[model](query, many=is_many).data
            response = shipJson(payload)
            return JsonResponse(response)
        except:
            return HttpJsonResponse(404)

    def put(self, request: 'HttpRequest', model: str, key: str,
            value: str) -> JsonResponse:
        # if not request.is_ajax():
        #   return HttpJsonResponse(404)
        if not permissionCheck(request.user, model, 'edit'):
            return HttpJsonResponse(403)
        if modelCheck(model):
            return HttpJsonResponse(403)
        try:
            model_object = data_models[model]
            instance = model_object.objects.get(Q((key, value)))
            data = JSONParser().parse(request)
            new_data = model_serializers[model](instance, data=data)
            if new_data.is_valid():
                new_data.save()
                return HttpJsonResponse(202)
            return HttpJsonResponse(400)
        except:
            return HttpJsonResponse(404)

    def post(self, request: 'HttpRequest', model: str):
        # if not request.is_ajax():
        #   return HttpJsonResponse(404)
        # if not permissionCheck(request.user, model, 'create'):
        #    return HttpJsonResponse(403)
        # if modelCheck(model):
        # return HttpJsonResponse(403)
        print('yes')
        try:
            new_data = model_serializers[model](
                data=JSONParser().parse(request.POST))
            print(new_data)
            if new_data.is_valid():
                new_data.save()
                return HttpJsonResponse(201)
            return HttpJsonResponse(400)
        except:
            return HttpJsonResponse(404)

    def delete(self, request: 'HttpRequest', model: str, key: str,
               value: str) -> JsonResponse:
        # if not request.is_ajax():
        #   return HttpJsonResponse(404)
        if not permissionCheck(request.user, model, 'delete'):
            return HttpJsonResponse(403)
        if modelCheck(model):
            return HttpJsonResponse(403)
        try:
            model_object = data_models[model]
            instance = model_object.objects.get(Q((key, value)))
            instance.delete()
            return HttpJsonResponse(202)
        except:
            return HttpJsonResponse(404)

# @login_required
# @ensure_csrf_cookie
# @requires_csrf_token
# @csrf_protect


def searchSQL(request: 'HttpRequest', route: str, table: str) -> JsonResponse:
    # if not request.is_ajax():
    #   return HttpJsonResponse(404)
    if request.method != 'GET':
        return HttpJsonResponse(400)
    if 'all' in route:
        if not ('limiter' in route):
            query = f"SELECT * from dbapi_{table}"
            payload = data_models[table].objects.raw(query)
            return shipJson(payload)
        route = route.split('/')
        ptr = route.index('limiter')
        limiter = route[ptr+1]
        constraint = route[ptr+2]
        query = f"SELECT * FROM dbapi_{table} {limiter} {constraint}"
        payload = data_models[table].objects.raw(query)
        return shipJson(payload)
    if not ('limiter' in route):
        fields = route.replace('/', ' ,')
        query = f"SELECT {fields} FROM dbapi_{table}"
        payload = data_models[table].objects.raw(query)
        return shipJson(payload)
    route = route.split('/')
    ptr = route.index('limiter')
    limiter = route[ptr+1]
    constraint = route[ptr+2]
    route.remove('limiter')
    route.remove(limiter)
    route.remove(constraint)
    fields = ','.join(route)
    query = f"SELECT {fields} FROM dbapi_{table} {limiter} {constraint}"
    payload = data_models[table].objects.raw(query)
    return shipJson(payload)

# @login_required


@lru_cache(maxsize=256)
# @ensure_csrf_cookie
# @requires_csrf_token
# @csrf_protect
def diveSearch(request: 'HttpRequest') -> JsonResponse:
    # if not request.is_ajax():
    #   return HttpJsonResponse(404)
    if request.method != "POST":
        return HttpJsonResponse(400)
    try:
        request = request.data  # type: Dict
        supermodel = request['supermodel']['model']
        key_pair = (request['supermodel']['key'],
                    request['supermodel']['value'])
        parentmodel = data_models[supermodel].get(Q(key_pair))

        def recursiveSearchTree(supermodel, submodels, n=0):
            if n == len(submodels):
                return supermodel
            supermodel_set = getattr(
                supermodel, f"{submodels[n]['model']}_set")
            updated_supermodel = supermodel_set.get(
                Q((submodels[n]['key'], submodels[n]['value'])))
            del supermodel_set, supermodel
            return recursiveSearchTree(updated_supermodel, submodels, n+1)
        result = recursiveSearchTree(parentmodel, request['submodels'])
        payload = model_serializers[result._meta.model_name](result).data
        return JsonResponse(shipJson(payload), safe=False)
    except:
        return HttpJsonResponse(404)
