import json
import plotly.express as px
import plotly.utils


def test(chart_type="pie"):
    df = px.data.gapminder().query("year == 2007").query("continent == 'Europe'")
    df.loc[df['pop'] < 2.e6, 'country'] = 'Other countries'
    if chart_type == "pie":
        fig = px.pie(df, values='pop', names='country', title='Population of European continent')
    elif chart_type == "bar":
        fig = px.bar(df, x="country", y="pop", title="Population of European continent")
    else:
        fig = ""

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON
