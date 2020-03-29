import altair as alt
from vega_datasets import data
from countries import FROM_COUNTRY
import pandas as pd
import numpy as np


def make_data_long(df_long):
    data_long = (df_long
                 .fillna(method='ffill')
                 .replace(0, np.nan)
                 .dropna()
                 .reset_index()
                #  .pipe(lambda f: pd.concat([f, f.groupby(['date', 'kind'])['count'].sum().reset_index().assign(country='all')]))
                )
    return data_long

def make_ts_selections(data_long):
    selection_legend = alt.selection_single(fields=['kind'], bind='legend', empty='all')

    selection_tooltip = alt.selection_single(fields=['date'], 
                                             nearest=True, 
                                             on='mouseover', 
                                             empty='none', 
                                             clear='mouseout')
    
    return selection_legend, selection_tooltip

def make_ts_chart(data_long, selection_legend, selection_tooltip):
    base = (alt
            .Chart(data_long)
            .encode(x='date:T')
           )

    lines = (base
             .mark_line(point=False)
             .encode(
                alt.Color(
                    'kind:N', 
                    scale=alt.Scale(
                        domain=['confirmed', 'recovered', 'deaths'], 
                        range=['orange', 'green', 'black'])),
                y='count:Q',
             )
            )

    points = lines.mark_point().transform_filter(selection_tooltip)

    rule = (base
            .transform_pivot('kind', value='count', groupby=['date'])
            .mark_rule()
            .encode(
                opacity=alt.condition(selection_tooltip, alt.value(0.3), alt.value(0)),
                tooltip=[
                    alt.Tooltip(c, type='quantitative')
                    for c in sorted(data_long.kind.unique())]
                    # + [alt.Tooltip('date', type='temporal')]
                    )
            .add_selection(selection_tooltip)
           )

    chart = ((lines.encode(opacity=alt.condition(selection_legend, alt.value(1), alt.value(0.2)))
             + rule
             + points)
             .add_selection(selection_legend))
    return chart

kind_schemes = {
    'deaths': 'greys', 
    'recovered': 'greens', 
    'confirmed': 'reds'
}

countries = alt.topo_feature(data.world_110m.url, 'countries')

def make_map_data(data_long, countries):
    data_long_map = (data_long
                    .assign(country_code=lambda f: f['country'].map(FROM_COUNTRY).astype(pd.Int64Dtype()))
                    .dropna(subset=['country_code'])
                    .assign(id=lambda f: f.country_code.astype(int))
                    .drop('country_code', axis=1)
                    ) 
                    
    map_data = (data_long_map
                .groupby(['country', 'kind'])
                .last()
                .reset_index()
                .assign(scheme=lambda f: f['kind'].map(kind_schemes))
                .assign(day=lambda f: f['date'].dt.dayofyear)
            )
    return map_data



def make_map(map_data, kind_schemes):
    # selection_kind = alt.selection_single(
    #     fields=['kind'],
    #     name='kind',
    #     empty='all', 
    #     bind=alt.binding_select(options=sorted(['deaths', 'confirmed', 'recovered']))
    # )

    slider = alt.binding_range(min=int(map_data.day.min()),
                               max=int(map_data.day.max()),
                               step=1)

    select_day = alt.selection_single(name='day',
                                       fields=['day'],
                                       bind=slider,
                                      on='none',
                                     init={'day': int(map_data.day.max())}
                                     )
    def make_base():
        base = (alt
             .Chart(countries)
                .encode(
                    tooltip=['count:Q', 'country:N', 'date:T', 'day:Q'])
                .mark_geoshape(stroke='white', strokeWidth=0.5)
        .encode(color=alt.Color('count:Q', scale=alt.Scale(scheme='reds')))
        .transform_lookup(
            lookup='id',
            from_=alt.LookupData(data=map_data.query('kind ==  "confirmed"'),
                                    key='id', 
                                    fields=['count', 'kind', 'country', 'day', 'date'])
        )
        # .add_selection(selection_legend_map)
        # .transform_filter(selection_legend_map)
               )
        return base

    base = make_base()
    # charts = dict()
    # for kind, scheme in kind_schemes.items():
    #     charts[kind] = (base
    #                     .encode(color=alt.Color('count:Q', scale=alt.Scale(scheme=scheme)))
    #                     .transform_lookup(
    #                         lookup='id',
    #                         from_=alt.LookupData(data=map_data.query('kind == @kind'), 
    #                                              key='id', 
    #                                              fields=['count', 'kind', 'country', 'day', 'date'])
    #                     )
    #                     .properties(title=kind)
    #                 #    .add_selection(select_day)
    #                 #    .transform_filter(select_day)
    #                    )

    # chart = (alt.vconcat(*charts.values())
    #          .resolve_scale(color='independent')
    #         #  .properties(
    #         #             autosize=alt.AutoSizeParams(
    #         #                 type='fit-x',
    #         #                 contains='padding')
    #         #                 )
    #         )
    return base#.add_selection(selection_kind).transform_filter(selection_kind)
    