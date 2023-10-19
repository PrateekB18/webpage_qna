from dash import html, dcc
import dash_bootstrap_components as dbc

navbar = dbc.NavbarSimple(
                    children=[
                        dbc.NavItem(dcc.Link(html.I(className="fab fa-linkedin"), href="https://www.linkedin.com/in/prateekbahl/")),
                        html.Span(" ", style={"width": "20px"}),
                        dbc.NavItem(dcc.Link(html.I(className="fab fa-github"), href="https://github.com/PrateekB18/")),
                    ],
                    brand="Webpage Q&A",
                    brand_href="#",
                    color="#e3f2fd",
                    dark=False,
                    
                )
