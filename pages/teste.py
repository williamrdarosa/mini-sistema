import dash
from dash import html

dash.register_page(__name__, path='/teste', path_template="/teste/<report_id>")


def layout(report_id=None):
    if report_id == None:
        return html.Div(
            f"The user requested report ID: 0."
        )
    return html.Div(
        f"The user requested report ID: {report_id}."
    )
