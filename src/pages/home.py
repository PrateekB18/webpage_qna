# package imports
import dash
from dash import callback, Input, Output, State
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from components import TextVectorizer, QnAProcessor 
from urllib.parse import urlparse

dash.register_page(
    __name__,
    path='/',
    redirect_from=['/home'],
    title='LLM Q&A'
)

layout = dmc.MantineProvider([
                        dmc.Stack([
                            dmc.Text("A web application powered by OpenAI GPT-3.5 and HuggingFace sentence transformers, designed to answer questions based on the content of webpages. You can provide up to three URLs for scraping the content. Links are processed using LangChain and content is retrieved using Facebook AI Similarity Search. To use the question-answer feature, you need to provide your OpenAI API key.", size="md"),
                            dmc.Grid(
                                children=[
                                    dmc.Col(dmc.TextInput(
                                                        type="text",
                                                        radius="xl",
                                                        id="api-key",
                                                        placeholder="Your OpenAI API Key",
                                                        icon=DashIconify(icon="solar:key-broken"),
                                                    ), 
                                            
                                            span=5),
                                    dmc.Col(dmc.ActionIcon(
                                                        DashIconify(icon="solar:recive-square-broken", width=25),
                                                        size="xl",
                                                        variant="light",
                                                        color="blue",
                                                        radius="xl",
                                                        id="api-key-submit",
                                                    ),
                                            
                                            span=1),
                                ],
                                justify="center",
                                align="center",
                                gutter="sm",
                            ),
                            dmc.Space(h=10),
                            dmc.Grid(
                                children=[
                                    dmc.Col(
                                            dmc.Stack([
                                                            dmc.TextInput(
                                                                type="text",
                                                                radius="xl",
                                                                id="url-1",
                                                                placeholder="First URL",
                                                                icon=DashIconify(icon="solar:link-broken"),
                                                            ),
                                                            dmc.Space(h=2),
                                                            dmc.TextInput(
                                                                type="text",
                                                                radius="xl",
                                                                id="url-2",
                                                                placeholder="Second URL",
                                                                icon=DashIconify(icon="solar:link-broken"),
                                                            ),
                                                            dmc.Space(h=2),
                                                            dmc.TextInput(
                                                                type="text",
                                                                radius="xl",
                                                                id="url-3",
                                                                placeholder="Third URL",
                                                                icon=DashIconify(icon="solar:link-broken"),
                                                            ),
                                                            dmc.Space(h=13),
                                                            
                                                            dmc.Button(
                                                                    "Process Links",
                                                                    radius="xl",
                                                                    id="url-submit-button",
                                                                    size="md",
                                                                    leftIcon=DashIconify(icon="material-symbols:downloading-rounded", width=25),
                                                                ),
                                                        ]),
                                            
                                            span=5),
                                    
                                    dmc.Col(
                                            dmc.Stack([
                                                dmc.Grid(
                                                    children=[
                                                        dmc.Col(dmc.Textarea(
                                                                            placeholder="Question?",
                                                                            autosize=True,
                                                                            id="query",
                                                                            radius="xl",
                                                                            minRows=1,
                                                                        ), 
                                                                
                                                                span=11),
                                                        dmc.Col(dmc.ActionIcon(
                                                                            DashIconify(icon="mingcute:send-line", width=30),
                                                                            size="xl",
                                                                            id="query-submit",
                                                                            variant="filled",
                                                                            color="blue",
                                                                            radius="xl",
                                                                        ),
                                                                
                                                                span=1),
                                                    ],
                                                    justify="center",
                                                    align="center",
                                                    gutter="sm",
                                                ),
                                                    dmc.Container(  " ",
                                                                    id = "output",
                                                                    style={
                                                                        "border": f"1px solid {dmc.theme.DEFAULT_COLORS['gray'][4]}",
                                                                        "border-radius": "22px",
                                                                        "height": 205,
                                                                        "width":"100%",
                                                                        "overflow": "scroll"
                                                                        }
                                                                    ),
                                                ]),
                                            
                                            span="auto"),
                                ],
                                justify="center",
                                align="center",
                                gutter="lg",
                            ),
                            dmc.Space(h=10),
                            dmc.Grid(
                                    children=[
                                        dmc.Button(
                                                        "Reset",
                                                        radius="xl",
                                                        id="reset-button",
                                                        size="md",
                                                        variant="outline",
                                                        leftIcon=DashIconify(icon="system-uicons:reset-alt", width=25),
                                                    ),
                                        ],
                                        justify="center",
                                        align="center"                          
                            ),
                        ])
                    ]),

@callback(
    Output("api-key","disabled"),
    [Input("api-key-submit", "n_clicks"),
    Input("api-key","value")]
)

def get_api_key(button_click, api_key):
    if (button_click is not None) & (len(api_key)>50):
        return True
    
@callback(
    [Output("url-1","disabled"),
    Output("url-2","disabled"),
    Output("url-3","disabled"),
    Output("url-submit-button", "leftIcon")],
    [Input("url-submit-button", "n_clicks"),
    Input("url-1","value"),
    Input("url-2","value"),
    Input("url-3","value")]
)

def process_urls(url_button_click, url_1, url_2, url_3):
    urls = [url_1,url_2,url_3]
    
    valid_urls = []
    for url in urls:
        parsed_url = urlparse(url)
        if parsed_url.scheme and parsed_url.netloc:
            valid_urls.append(url)
    if (url_button_click is not None) & (len(valid_urls)>0):
        return True, True, True, DashIconify(icon="line-md:downloading-loop", width=25)
    else:
        return False, False, False, DashIconify(icon="material-symbols:downloading-rounded", width=25)
    
@callback(
    Output("url-submit-button", "leftIcon", allow_duplicate=True),
    [Input("url-submit-button", "n_clicks")],
    [State("url-1", "value"),
     State("url-2", "value"),
     State("url-3", "value")],
    prevent_initial_call=True
)
def process_text_vectorization(url_button_click, url_1, url_2, url_3):
    left_icon = DashIconify(icon="material-symbols:downloading-rounded", width=25)

    if url_button_click is not None:
        urls = [url_1, url_2, url_3]

        valid_urls = []
        for url in urls:
            parsed_url = urlparse(url)
            if parsed_url.scheme and parsed_url.netloc:
                valid_urls.append(url)

        if len(valid_urls) > 0:
            text_vectorizer = TextVectorizer(valid_urls)
            text_vectorizer.process_text()
            text_vectorizer.create_embeddings()
            text_vectorizer.create_vector_index()
            left_icon = DashIconify(icon="material-symbols:downloading-rounded", width=25)

    return left_icon



@callback(
    [Output("output", "children"),
    Output("query-submit", "n_clicks"),
    Output("query-submit", "children", allow_duplicate=True)],
    [Input("api-key", "value"),
    Input("query", "value"),
    Input("query-submit", "n_clicks")],
    prevent_initial_call=True
)

def QnA_Output(api, query, submit):
    if submit is not None:
        submit = None
        if not api:
            output_text = "Please provide OpenAI API"
        elif not query:
            output_text = "No Question Asked. Ask a Question and Click send."
        else:
            qna_processor = QnAProcessor(api)
            output = qna_processor.answer_question(query)
            answer = output["answer"]
            source = output["sources"]
            output_text = f"{answer}\n\nSource: {source}"
            
        return f"{output_text}", submit, DashIconify(icon="mingcute:send-line", width=30)
    else:
        submit = None
        return "", submit, DashIconify(icon="mingcute:send-line", width=30)

@callback(
    [Output("url-1","disabled", allow_duplicate=True),
    Output("url-2","disabled", allow_duplicate=True),
    Output("url-3","disabled", allow_duplicate=True),
    Output("api-key","disabled", allow_duplicate=True)],
    Input("reset-button", "n_clicks"),
    prevent_initial_call=True
)

def reset(reset_button):
    if reset_button is not None:
        reset_button = None
        return False, False, False, False