
from django.template.loader import render_to_string
from weasyprint import HTML


def generate_users_pdf(data):
    rendered = render_to_string(
        'users/users_report.html',
        data
    )

    html = HTML(
        string=rendered
    )

    return html.write_pdf()
