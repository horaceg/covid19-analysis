import sys

import altair as alt

from charts import make_ts_chart, make_ts_selections, make_data_long
from charts import make_map, kind_schemes, make_map_data, countries, make_map_data
from fetch import fetch_timeseries, TS_URL

def make_chart(df_long):
    data_long = make_data_long(df_long)
    selection_legend, selection_tooltip = make_ts_selections(data_long)
    ts_chart = make_ts_chart(data_long, *make_ts_selections(data_long))
    ts_chart

    # Map

    map_data = make_map_data(data_long, countries)
    map_chart = make_map(map_data, kind_schemes)

    selection_country_click = alt.selection_single(
        fields=['country'],
        name='Country of',
        empty='all',
    )

    chart = (map_chart
    .encode(color=alt.condition(selection_country_click, 'count:Q', alt.value('lightgray'), scale=alt.Scale(scheme='reds', type= 'log', base=10)))
    .add_selection(selection_country_click)
    .add_selection(selection_legend)
    .transform_filter(selection_legend)
            .properties(width=650, height=400)
    | 
            ts_chart.add_selection(selection_country_click)
            .transform_filter(selection_country_click)
            .transform_aggregate(
                count='sum(count)',
                groupby=['kind', 'date']
            ).properties(width=650, height=400)
    )
    return chart

if __name__ == "__main__":
    df = fetch_timeseries(TS_URL)
    df_long = df.stack().rename('count').rename_axis(index={None: 'kind'})

    alt.data_transformers.enable('default', max_rows=None)
    alt.renderers.enable('html')
    alt.themes.enable('fivethirtyeight')

    chart = make_chart(df_long)
    chart.save(sys.stdout, format='html')
