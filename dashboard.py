!pip install dash
import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output

# Load the dataset
file_path = "road_accident_dataset.csv"
df = pd.read_csv(file_path)

# Initialize the Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Road Accident Dashboard"),

    dcc.Dropdown(
        id='year-dropdown',
        options=[{'label': year, 'value': year} for year in sorted(df['Year'].unique())],
        value=df['Year'].min(),
        clearable=False
    ),

    dcc.Graph(id='accident-severity-pie'),
    dcc.Graph(id='accidents-over-time'),
    dcc.Graph(id='accident-causes-bar')
])

@app.callback(
    Output('accident-severity-pie', 'figure'),
    [Input('year-dropdown', 'value')]
)
def update_pie_chart(selected_year):
    filtered_df = df[df['Year'] == selected_year]
    fig = px.pie(filtered_df, names='Accident Severity', title=f'Accident Severity Distribution in {selected_year}')
    return fig

@app.callback(
    Output('accidents-over-time', 'figure'),
    [Input('year-dropdown', 'value')]
)
def update_line_chart(selected_year):
    filtered_df = df[df['Year'] == selected_year]
    time_data = filtered_df.groupby('Month').size().reset_index(name='Accidents')
    fig = px.line(time_data, x='Month', y='Accidents', title=f'Accidents Over Time in {selected_year}')
    return fig

@app.callback(
    Output('accident-causes-bar', 'figure'),
    [Input('year-dropdown', 'value')]
)
def update_bar_chart(selected_year):
    filtered_df = df[df['Year'] == selected_year]
    cause_data = filtered_df['Accident Cause'].value_counts().reset_index()
    cause_data.columns = ['Accident Cause', 'Count']
    fig = px.bar(cause_data, x='Accident Cause', y='Count', title=f'Accident Causes in {selected_year}')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
