import re
import pandas as pd
import altair as alt
from vega_datasets import data

from countries import FROM_COUNTRY


def fetch_google():
    df = pd.read_csv('https://www.gstatic.com/covid19/mobility/Global_Mobility_Report.csv', parse_dates=['date'])

    def safe_match(pat, text):
        match = re.match(pat, text)
        return match.groups()[0] if match else text

    df.columns = df.columns.map(lambda col: safe_match("(.*)_percent", col))
    # google_mobility = (google_mobility
    #             .merge(isocodes, left_on='country_region_code', right_on='alpha-2_code', how='left')
    #             .merge(location_code, left_on='alpha-3_code', right_on='iso_code', how='left'))

    df = (df.loc[lambda f: f['sub_region_1'].isna() & f["sub_region_2"].isna()]
          .rename({'country_region': 'country'}, axis=1)
                       .set_index(['country', 'date'])
                       [['retail_and_recreation', 'grocery_and_pharmacy', 'parks', 'transit_stations', 'workplaces', 'residential']]
                       .rename_axis('category', axis=1)
                       .stack()
                       .rename('value')
                       .sort_index()
                       .groupby(["country", "category"])
                       .apply(lambda g: g.reset_index(["country", "category"], drop=True).rolling("7d").mean())
                       .reset_index()
                       )
    # .set_index(['iso_code', 'date']).select_dtypes(float).div(100)

    df = df.assign(country_code=df['country'].map(FROM_COUNTRY))
    return df

def make_chart(df, world_topo):
    categories = list(df.category.unique())
    map_data = (df
                .set_index(['country', 'country_code', 'category'])
                ['value']
                .div(100)
                .groupby(['country', 'country_code', 'category'])
                .last()
                .unstack()
                .reset_index())

    input_dropdown = alt.binding_select(options=categories)
    selection_category = alt.selection_single(fields=['category'], 
                                            bind=input_dropdown, 
                                            name='Mobility',
                                            init={'category': 'workplaces'})

    selection_country = alt.selection_multi(
            fields=['country'],
            name='Country of',
            empty='all',
    #     init={'country': 'France'}
        )

    background = (alt.Chart(world_topo)
                .mark_geoshape(fill='lightgray', stroke='white', strokeWidth=0.5)
                .transform_filter('datum.id != 10')
    #               .transform_filter('datum.id != 304')
                )

    foreground = (alt.Chart(world_topo)
            .mark_geoshape(stroke='white', strokeWidth=0.5)
            .encode(
                color=alt.condition(
                    selection_country,
                    alt.Color('value:Q', scale=alt.Scale(scheme='blueorange', domainMid=0), legend=alt.Legend(format=".0%")),
                    alt.value('lightgray')
                ),
                tooltip=[alt.Tooltip('value:Q', format='.0%'), 'country:N']
            )
                .transform_lookup(
                    lookup='id',
                    from_=alt.LookupData(data=map_data,
                                    key='country_code', 
                                    fields=['country'] + categories)
                )
                .transform_fold(
                    fold=categories,
                    as_=['category', 'value']
                )
                .add_selection(selection_category)
                .transform_filter(selection_category)
                ).add_selection(selection_country)

    map_chart = (background + foreground).properties(width=700, height=500, 
    #                                                  title="Variation to baseline on March 29"
                                                    )

    ts_data = df.assign(value=lambda f: f['value'].div(100))
    base_ts = alt.Chart(ts_data)

    ts_chart = (base_ts
                .mark_line(point=True)
                .encode(x='date:T', 
                        y=alt.Y('value:Q', axis=alt.Axis(format='%')), 
                        tooltip=[alt.Tooltip('date:T', format='%a, %b %e'), alt.Tooltip('value:Q', format='.1%')])
    #             .properties(title='Variation through time')
            .add_selection(selection_category)
                .add_selection(selection_country)
                .transform_filter(selection_category)
                .transform_filter(selection_country)
                .transform_aggregate(
                    value='mean(value)',
                    groupby=['category', 'date']
                )
            )

    chart = (ts_chart | map_chart).properties(title='Mobility change by geography, across different categories of places (Variation to baseline)')
    return chart

def main():
    df = fetch_google()
    world_topo = alt.topo_feature(data.world_110m.url, 'countries')
    chart = make_chart(df, world_topo)
    chart.save('dist/static/mobility/charts/map.html')

if __name__ == "__main__":
    main()
