from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from apps.hello.models import Greeting, Response


def hello_world(request: HttpRequest) -> HttpResponse:
    greeting = Greeting.objects.order_by("-created_at").first()
    if greeting:
        responses = greeting.responses.all()
    else:
        responses = Response.objects.none()
    return render(
        request,
        "hello/hello_world.html",
        {
            "greeting": greeting,
            "responses": responses,
        },
    )


def create_greeting(request: HttpRequest) -> HttpResponse:
    """Create a new greeting."""
    error = None
    if request.method == "POST":
        message = request.POST.get("message", "").strip()
        if message:
            greeting = Greeting.objects.create(message=message)
            return redirect("greeting_detail", greeting_id=greeting.id)
        else:
            error = "Message cannot be empty."
    return render(request, "hello/create_greeting.html", {"error": error})


def greeting_detail(request: HttpRequest, greeting_id: int) -> HttpResponse:
    """Display a specific greeting with its responses and allow adding new responses."""
    try:
        greeting = Greeting.objects.get(id=greeting_id)
    except Greeting.DoesNotExist:
        return render(request, "hello/greeting_not_found.html")
    responses = greeting.responses.all()
    return render(
        request,
        "hello/greeting_detail.html",
        {
            "greeting": greeting,
            "responses": responses,
        },
    )


def add_response(request: HttpRequest, greeting_id: int) -> HttpResponse:
    """Add a response to a greeting."""
    error = None
    if request.method == "POST":
        try:
            greeting = Greeting.objects.get(id=greeting_id)
        except Greeting.DoesNotExist:
            return render(request, "hello/greeting_not_found.html")
        author_name = request.POST.get("author_name", "").strip()
        reply = request.POST.get("reply", "").strip()
        if author_name and reply:
            Response.objects.create(
                greeting=greeting, reply=reply, author_name=author_name
            )
            return redirect("greeting_detail", greeting_id=greeting_id)
        else:
            error = "Both name and reply are required."
            responses = greeting.responses.all()
            return render(
                request,
                "hello/greeting_detail.html",
                {
                    "greeting": greeting,
                    "responses": responses,
                    "error": error,
                },
            )
    return redirect("greeting_detail", greeting_id=greeting_id)


def list_greetings(request: HttpRequest) -> HttpResponse:
    """List all greetings."""
    greetings = Greeting.objects.all().order_by("-created_at")
    return render(
        request,
        "hello/list_greetings.html",
        {"greetings": greetings},
    )
