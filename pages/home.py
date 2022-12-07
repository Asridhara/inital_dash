from dash import dcc, register_page, html
import dash_mantine_components as dmc
import dash_bootstrap_components  as dbc
import  dash

register_page(__name__, path="/", icon="fa-solid:home",)

layout = dmc.Container(
    [
        dmc.Title("Welcome to the home page", order=4 , align= "center"),

        dbc.Card(
            dbc.CardBody("This is a demo of a basic multi-page app for data analysis, monitoring and generating reports"),
        ),
        # dmc.Paper(
        #     children =[
        #         html.Textarea(
        #             'This is a demo of a multi-page app with nested folders in the `pages` folder.'  
        #         )  
        #     ]
        # ),
        
    ]
)