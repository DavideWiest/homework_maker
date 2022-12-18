from django.http import HttpResponse
from .apihelper import UrlQueryManager, BadRequestError
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .apihelper import successful_authentication, AUTH_ERR
from .api_funcs import ApiFunctions
from wsgiref.util import FileWrapper


af = ApiFunctions()

@api_view()
def status(request):
    if not successful_authentication(request):
        return Response(AUTH_ERR)

    response = {"status": "ok"}

    return Response(response)

@api_view()
def text_to_tasks(request):
    if not successful_authentication(request):
        return Response(AUTH_ERR)

    if "text" not in request.GET:
        return Response({"status": "error", "error": "text key must be given"})
    
    text = request.GET.get("text")
    response = {"tasks": af.text_to_tasks(text)}

    return Response(response)

@api_view()
def tasks_to_answers_pdf(request):
    if not successful_authentication(request):
        return Response(AUTH_ERR)

    if "tasks" not in request.GET:
        return Response({"status": "error", "error": "tasks key must be given"})
    


    answers = af.tasks_to_answers(request.GET.get("tasks"))

    params = {
        "title": request.GET.get("title", "Homework"),
        "info": request.GET.get("info", " "),
        "tasks": {
            request.GET.get("tasks")[i]: answers[i] for i in len(request.GET.get("tasks"))
        }
    }
    
    pdf = af.answers_to_pdf(params)

    return HttpResponse(FileWrapper(pdf), content_type='application/pdf')

# @api_view()
# def answers_to_pdf(request):
#     if not successful_authentication(request):
#         return Response(AUTH_ERR)

#     response = {"status": "ok"}

#     return Response(response)

