from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import plotly.express as px
from io import BytesIO
import base64

app = Flask(__name__)

# Global variable to store DataFrame
df = None

@app.route('/', methods=['GET', 'POST'])
def index():
    global df

    if request.method == 'POST':
        file = request.files['file']
        if file:
            if file.filename.endswith(".csv"):
                df = pd.read_csv(file)
            elif file.filename.endswith(".xlsx"):
                df = pd.read_excel(file)

    if df is not None:
        columns = list(df.columns)
        x_column = request.form.get('x_column', columns[0])
        y_column = request.form.get('y_column', columns[1])

        fig = create_plot(x_column, y_column)
        plot_div = plot_to_div(fig)

        return render_template('index.html', columns=columns, x_column=x_column, y_column=y_column, plot_div=plot_div)

    return render_template('index.html')

def create_plot(x_column, y_column):
    fig = px.scatter(df, x=x_column, y=y_column, title=f'{x_column} vs {y_column}')
    return fig

def plot_to_div(fig):
    img_data = BytesIO()
    fig.write_html(img_data, include_plotlyjs='cdn')
    plot_div = base64.b64encode(img_data.getvalue()).decode()
    return plot_div

if __name__ == '__main__':
    app.run(debug=True)
