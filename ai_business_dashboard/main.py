# main.py
import dash
from dash import dcc, html, Input, Output
import dash_daq as daq
import dash_extensions as de
import plotly.express as px
import pandas as pd

# ---------------- Sample Data ----------------
data = pd.DataFrame({
    "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]*3,
    "Category": ["Electronics"]*6 + ["Clothing"]*6 + ["Furniture"]*6,
    "Sales": [12000, 15000, 17000, 14000, 18000, 20000,
              8000, 7000, 9000, 8500, 9500, 10000,
              5000, 6000, 5500, 6500, 7000, 7500]
})

# ---------------- Initialize App ----------------
app = dash.Dash(__name__)
app.title = "AI Business Analytics Dashboard"

# ---------------- App Layout ----------------
app.layout = html.Div(style={'font-family': 'Arial, sans-serif', 'background-color': '#fdf6f0'}, children=[

    # Header
    html.Div("AI Business Analytics Dashboard", style={
        'background-color': '#ffb3ba', 'color': '#000', 'padding': '20px',
        'font-size': '28px', 'font-weight': 'bold', 'text-align': 'center'
    }),

    # Animated KPI section
    html.Div(
        style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center', 'gap': '20px',
               'marginTop': '10px', 'marginBottom': '20px'},
        children=[
            de.Lottie(
                id="sales-animation",
                options={
                    "path": "https://assets10.lottiefiles.com/packages/lf20_9wq6a8.json",
                    "loop": True,
                    "autoplay": True
                },
                width="100px",
                height="100px"
            ),
            daq.LEDDisplay(
                id='total-sales',
                label='Total Sales',
                value=data['Sales'].sum(),
                color="#FF5E57",
                size=30
            ),
            de.Lottie(
                id="category-animation",
                options={
                    "path": "https://assets4.lottiefiles.com/packages/lf20_touohxv0.json",
                    "loop": True,
                    "autoplay": True
                },
                width="80px",
                height="80px"
            )
        ]
    ),

    html.Div(style={'display': 'flex'}, children=[

        # Sidebar
        html.Div(style={'width': '20%', 'background-color': '#ffdfba', 'padding': '15px'}, children=[
            html.H3("Filters", style={'color': '#000'}),
            html.Label("Select Category:"),
            dcc.Dropdown(
                id='category-dropdown',
                options=[{'label': c, 'value': c} for c in data['Category'].unique()],
                value='Electronics'
            ),
            html.Br(),
            html.Label("Select Month:"),
            dcc.Dropdown(
                id='month-dropdown',
                options=[{'label': m, 'value': m} for m in data['Month'].unique()],
                value='Jan'
            ),
            html.Br(),
            html.Button("Toggle Dark Mode", id='toggle-theme', n_clicks=0, style={'width': '100%'})
        ]),

        # Main content
        html.Div(style={'width': '80%', 'padding': '15px'}, children=[
            html.H3("Sales Overview", style={'color': '#000'}),
            dcc.Graph(id='sales-bar-chart'),
            html.H3("Category Distribution", style={'color': '#000'}),
            dcc.Graph(id='category-pie-chart')
        ])
    ])
])

# ---------------- Callbacks ----------------
@app.callback(
    Output('sales-bar-chart', 'figure'),
    Output('category-pie-chart', 'figure'),
    Input('category-dropdown', 'value'),
    Input('month-dropdown', 'value'),
    Input('toggle-theme', 'n_clicks')
)
def update_charts(category, month, n_clicks):
    # Determine theme
    dark_mode = n_clicks % 2 == 1
    bg_color = '#2b2b2b' if dark_mode else '#fdf6f0'
    text_color = '#fff' if dark_mode else '#000'

    filtered = data[(data['Category'] == category) & (data['Month'] == month)]

    # Bar chart
    bar_fig = px.bar(filtered, x='Month', y='Sales', color='Category',
                     text='Sales', height=400)
    bar_fig.update_layout(plot_bgcolor=bg_color, paper_bgcolor=bg_color,
                          font_color=text_color)

    # Pie chart for category distribution in selected month
    pie_data = data[data['Month'] == month]
    pie_fig = px.pie(pie_data, names='Category', values='Sales', height=400)
    pie_fig.update_layout(plot_bgcolor=bg_color, paper_bgcolor=bg_color,
                          font_color=text_color)

    return bar_fig, pie_fig

# ---------------- Run App ----------------
if __name__ == '__main__':
    app.run_server(debug=True)
