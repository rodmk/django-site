from django.http import HttpRequest, HttpResponse

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

    return HttpResponse(html)
