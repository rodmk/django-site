from django.http import HttpRequest, HttpResponse
from django.middleware.csrf import get_token
from django.shortcuts import redirect

from apps.hello.models import Greeting, Response


def hello_world(request: HttpRequest) -> HttpResponse:
    # Get or create a greeting
    greeting, created = Greeting.objects.get_or_create(
        message="Hello, World!", defaults={"message": "Hello, World!"}
    )

    # Create some sample responses if this is a new greeting
    if created:
        Response.objects.create(
            greeting=greeting, reply="Hi there!", sender_name="Alice"
        )
        Response.objects.create(
            greeting=greeting, reply="How are you?", sender_name="Bob"
        )

    # Get all responses for this greeting
    responses = greeting.responses.all()
    # Build HTML response demonstrating foreign key access
    html = f"<h1>{greeting.message}</h1>"
    html += f"<p>Greeting created: {greeting.created_at}</p>"
    html += "<h2>Responses:</h2><ul>"

    for response in responses:
        # These property accesses should be properly typed with django-stubs
        html += f"<li><strong>{response.sender_name}</strong>: {response.reply}"
        html += f" (replied to: '{response.greeting.message}' at {response.created_at})</li>"

    html += "</ul>"

    # Add navigation links
    html += "<h2>Actions:</h2>"
    html += f'<p><a href="/hello/greeting/{greeting.id}/">View/Reply to this greeting</a></p>'
    html += '<p><a href="/hello/create/">Create a new greeting</a></p>'
    html += '<p><a href="/hello/list/">View all greetings</a></p>'

    return HttpResponse(html)


def create_greeting(request: HttpRequest) -> HttpResponse:
    """Create a new greeting."""
    if request.method == "POST":
        message = request.POST.get("message", "").strip()
        if message:
            greeting = Greeting.objects.create(message=message)
            # Redirect to the greeting detail page
            return redirect("greeting_detail", greeting_id=greeting.id)
        else:
            return HttpResponse(
                "<h1>Error</h1><p>Message cannot be empty.</p>"
                '<p><a href="/hello/create/">Try again</a></p>'
            )

    # Show the form for creating a greeting
    csrf_token = get_token(request)
    html = f"""
    <h1>Create a New Greeting</h1>
    <form method="post">
        <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
        <label for="message">Message:</label><br>
        <input type="text" id="message" name="message" maxlength="200" required><br><br>
        <input type="submit" value="Create Greeting">
    </form>
    <p><a href="/hello/">Back to Hello World</a></p>
    """
    return HttpResponse(html)


def greeting_detail(request: HttpRequest, greeting_id: int) -> HttpResponse:
    """Display a specific greeting with its responses and allow adding new responses."""
    try:
        greeting = Greeting.objects.get(id=greeting_id)
    except Greeting.DoesNotExist:
        return HttpResponse("<h1>Greeting not found</h1>")

    responses = greeting.responses.all()

    # Build HTML response
    html = f"<h1>{greeting.message}</h1>"
    html += f"<p>Greeting created: {greeting.created_at}</p>"
    html += "<h2>Responses:</h2><ul>"

    for response in responses:
        html += f"<li><strong>{response.sender_name}</strong>: {response.reply}"
        html += f" (replied at {response.created_at})</li>"

    html += "</ul>"

    # Add form for creating new responses
    csrf_token = get_token(request)
    html += f"""
    <h2>Add a Response</h2>
    <form method="post" action="/hello/greeting/{greeting_id}/reply/">
        <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
        <label for="sender_name">Your name:</label><br>
        <input type="text" id="sender_name" name="sender_name" maxlength="100" required><br><br>
        <label for="reply">Your reply:</label><br>
        <textarea id="reply" name="reply" maxlength="200" required></textarea><br><br>
        <input type="submit" value="Add Response">
    </form>
    <p><a href="/hello/">Back to Hello World</a> | <a href="/hello/create/">Create New Greeting</a></p>
    """

    return HttpResponse(html)


def add_response(request: HttpRequest, greeting_id: int) -> HttpResponse:
    """Add a response to a greeting."""
    if request.method == "POST":
        try:
            greeting = Greeting.objects.get(id=greeting_id)
        except Greeting.DoesNotExist:
            return HttpResponse("<h1>Greeting not found</h1>")

        sender_name = request.POST.get("sender_name", "").strip()
        reply = request.POST.get("reply", "").strip()

        if sender_name and reply:
            Response.objects.create(
                greeting=greeting, reply=reply, sender_name=sender_name
            )
            # Redirect back to the greeting detail page
            return redirect("greeting_detail", greeting_id=greeting_id)
        else:
            return HttpResponse(
                "<h1>Error</h1><p>Both name and reply are required.</p>"
                f'<p><a href="/hello/greeting/{greeting_id}/">Try again</a></p>'
            )

    # If not POST, redirect to greeting detail
    return redirect("greeting_detail", greeting_id=greeting_id)


def list_greetings(request: HttpRequest) -> HttpResponse:
    """List all greetings."""
    greetings = Greeting.objects.all().order_by("-created_at")

    html = "<h1>All Greetings</h1>"

    if greetings:
        html += "<ul>"
        for greeting in greetings:
            response_count = greeting.responses.count()
            html += (
                f'<li><a href="/hello/greeting/{greeting.id}/">{greeting.message}</a> '
            )
            html += (
                f"({response_count} response{'s' if response_count != 1 else ''}) - "
            )
            html += f"Created: {greeting.created_at.strftime('%Y-%m-%d %H:%M')}</li>"
        html += "</ul>"
    else:
        html += "<p>No greetings found.</p>"

    html += '<p><a href="/hello/create/">Create a new greeting</a></p>'
    html += '<p><a href="/hello/">Back to Hello World</a></p>'

    return HttpResponse(html)
