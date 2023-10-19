# package imports
import dash
from dash import html
import dash_bootstrap_components as dbc
from flask import Flask
from components import navbar


server = Flask(__name__)
app = dash.Dash(
    __name__,
    server=server,
    use_pages=True,    
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        dbc.icons.FONT_AWESOME
    ], 
    meta_tags=[
        {   
            'name': 'viewport',
            'content': 'width=device-width, initial-scale=1'
        }
    ],
    suppress_callback_exceptions=True,
    title='Webpage Q&A'
)

def serve_layout():
    # '''Define the layout of the application'''
    return html.Div(
        [
            navbar,
            dbc.Container(
                dash.page_container,
                class_name='my-2',
                style = {"padding-top":"50px"}
            ),
        ]
    )


app.layout = serve_layout   # set the layout to the serve_layout function
server = app.server         # the server is needed to deploy the application

if __name__ == "__main__":
    app.run_server(debug=True, dev_tools_props_check=False)

