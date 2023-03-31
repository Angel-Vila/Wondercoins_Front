import json
import plotly.express as px
import plotly.utils


def test(datos, chart_type="pie"):
    print(chart_type)
    if chart_type == "pie":
        fig = px.pie(datos, values='data', names='keys', title='Monedas según material')
    elif chart_type == "bar":
        fig = px.bar(datos, x="keys", y="data", title="Monedas según material")
    else:
        fig = ""

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON
