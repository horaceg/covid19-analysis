import altair as alt
from vega_datasets import data
from countries import FROM_COUNTRY
import pandas as pd
import numpy as np


def make_data_long(df_long):
    data_long = (
        df_long.fillna(method="ffill")
        .replace(0, np.nan)
        .dropna()
        .reset_index()
        #  .pipe(lambda f: pd.concat([f, f.groupby(['date', 'status'])['count'].sum().reset_index().assign(country='all')]))
    )
    return data_long


def assign_dod(g):
    return g.assign(diff=g.diff().fillna(0)).assign(
        diff_rel=lambda gg: gg["diff"].div(gg["count"])
    )


def make_dod(df_long):
    return df_long.to_frame().groupby(["country", "status"]).apply(assign_dod)


def make_ts_selections():
    selection_legend = alt.selection_single(
        fields=["status"], bind="legend", empty="all", init={"status": "confirmed"}
    )

    selection_tooltip = alt.selection_single(
        fields=["date"],
        nearest=True,
        on="mouseover",
        empty="none",
        clear="mouseout",
    )

    return selection_legend, selection_tooltip


def make_ts_chart(base_ts, status_list, selection_legend, selection_tooltip):
    lines = base_ts.mark_line(point=True).encode(
        alt.Color(
            "status:N",
            scale=alt.Scale(
                domain=["confirmed", "recovered", "deaths"],
                range=["orange", "green", "black"],
            ),
        ),
        y="count:Q",
    )

    points = lines.mark_point().transform_filter(selection_tooltip)

    rule = (
        base_ts.transform_pivot("status", value="count", groupby=["date"])
        .mark_rule()
        .encode(
            opacity=alt.condition(selection_tooltip, alt.value(0.3), alt.value(0)),
            tooltip=[alt.Tooltip(c, type="quantitative") for c in status_list]
            # + [alt.Tooltip('date', type='temporal')]
        )
        .add_selection(selection_tooltip)
    )

    chart = (
        lines.encode(
            opacity=alt.condition(selection_legend, alt.value(1), alt.value(0.2))
        )
        + rule
        + points
    ).add_selection(selection_legend)
    return chart


status_schemes = {"deaths": "greys", "recovered": "greens", "confirmed": "reds"}

countries = alt.topo_feature(data.world_110m.url, "countries")


def make_map_data(data_long, countries):
    data_long_map = (
        data_long.assign(
            country_code=lambda f: f["country"]
            .map(FROM_COUNTRY)
            .astype(pd.Int64Dtype())
        )
        .dropna(subset=["country_code"])
        .assign(id=lambda f: f.country_code.astype(int))
        .drop("country_code", axis=1)
    )

    map_data = (
        data_long_map.groupby(["country", "status"])
        .last()
        .reset_index()
        .assign(scheme=lambda f: f["status"].map(status_schemes))
        .assign(day=lambda f: f["date"].dt.dayofyear)
    )
    return map_data


def make_map(map_data, status_schemes):
    map_data = (
        map_data.set_index(["country", "id", "day", "date", "status"])
        .unstack()["count"]
        .reset_index()
    )

    base = (
        alt.Chart(countries)
        .encode(tooltip=["count:Q", "country:N", "day:Q", "status:N"])
        .mark_geoshape(stroke="white", strokeWidth=0.5)
        .transform_lookup(
            lookup="id",
            from_=alt.LookupData(
                data=map_data,
                key="id",
                fields=["confirmed", "recovered", "deaths", "country", "day", "date"],
            ),
        )
        .transform_fold(
            fold=["confirmed", "recovered", "deaths"], as_=["status", "count"]
        )
    )

    return base


def make_dod_chart(dod_long):
    return (
        alt.Chart(dod_long.reset_index())
        .mark_bar(point=True)
        .encode(
            alt.Y(
                "diff",
                #                           axis=alt.Axis(format='%')
            ),
            x="date",
            color="status",
            tooltip=["diff", "diff_rel", "date"],
        )
        .properties(width=500, height=300, title="New cases")
        #             .transform_aggregate(
        #                 diff='sum(diff)',
        #                 groupby=['status', 'date']
        #             )
    )


def combine_map_ts(map_chart, ts_chart, dod_chart, selection_legend):
    selection_country = alt.selection_single(
        fields=["country"],
        name="Country of",
        empty="all",
    )

    map_chart2 = (
        map_chart.encode(
            color=alt.condition(
                selection_country,
                alt.Color(
                    "count:Q", scale=alt.Scale(scheme="oranges", type="log", base=10)
                ),
                alt.value("lightgray"),
            )
        )
        .add_selection(selection_country)
        .properties(
            width=670,
            # width='container',
            height=400,
            title="Confirmed cases",
        )
        .add_selection(selection_legend)
        .transform_filter(selection_legend)
    )

    ts_chart2 = (
        ts_chart.add_selection(selection_country)
        .transform_filter(selection_country)
        .transform_aggregate(count="sum(count)", groupby=["status", "date"])
        .properties(
            width=500,
            # width='container',
            height=400,
            title="Cumulated cases",
        )
    )

    dod_chart2 = (
        dod_chart.add_selection(selection_country)
        .transform_filter(selection_country)
        .transform_aggregate(
            diff="sum(diff)", diff_rel="sum(diff_rel)", groupby=["status", "date"]
        )
        .add_selection(selection_legend)
        .transform_filter(selection_legend)
        .encode(opacity=alt.condition(selection_legend, alt.value(1), alt.value(0.2)))
    )

    chart = map_chart2.properties(width=900, title="Last cumulative cases") & (
        ts_chart2.properties(width=500, height=300) | dod_chart2
    )
    return chart
