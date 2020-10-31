import sys

import altair as alt

from charts import make_ts_chart, make_ts_selections, make_data_long
from charts import (
    make_map,
    status_schemes,
    make_map_data,
    countries,
    make_map_data,
    combine_map_ts,
    make_dod,
    make_dod_chart,
)
from fetch import fetch_timeseries, TS_URL


def make_chart(df_long):
    data_long = make_data_long(df_long)
    dod_long = make_dod(df_long).reset_index()

    base_ts = alt.Chart(data_long).encode(x="date:T")
    selection_legend, selection_tooltip = make_ts_selections()
    ts_chart = make_ts_chart(
        base_ts, sorted(dod_long.status.unique()), selection_legend, selection_tooltip
    )

    map_data = make_map_data(data_long, countries)
    map_chart = make_map(map_data, status_schemes)

    dod_chart = make_dod_chart(dod_long)
    chart = combine_map_ts(map_chart, ts_chart, dod_chart, selection_legend)

    return chart


if __name__ == "__main__":
    df = fetch_timeseries(TS_URL)
    df_long = df.stack().rename("count").rename_axis(index={None: "status"})

    alt.data_transformers.enable("default", max_rows=None)
    alt.renderers.enable("html")
    alt.themes.enable("fivethirtyeight")

    chart = make_chart(df_long)

    if len(sys.argv) > 1:
        if sys.argv[1] == "json":
            chart.save(sys.stdout, format="json")
        else:
            chart.save(sys.stdout, format="html")
