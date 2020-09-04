import csv
import pandas as pd
import plotly.graph_objects as go


def plot_cases():
    df = pd.read_csv('./data/cases_timeline.csv', parse_dates=['date'])
    # df.set_index('date', inplace=True)
    # df = df.resample('D').ffill().reset_index()
    # print(df)
    fig = go.Figure([go.Scatter(
                    x=df['date'], y=df['cases'], mode='lines+markers', marker_color='#ffa600',
                    text=df['cases'], textposition='bottom center')])
    fig.update_layout(
        template="plotly_white",
        xaxis_range=['2020-08-25', '2020-09-13'],
        title={
            'text': "Covid-19 Cases at the U Campus",
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        xaxis_title="Reported COVID-19 Cases",
        yaxis_title="Cases",
        font_color="black",
        font_size=24,
        font_family="Calibri")
    fig.write_image("cases.png", width=1024, height=512)
# -------MAIN----------


def main():
    plot_cases()


if __name__ == "__main__":
    main()
