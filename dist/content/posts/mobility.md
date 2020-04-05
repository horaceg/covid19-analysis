---
title: "Mobility datasets are here"
date: 2020-04-04
draft: true
---

Full timeseries data from Google's mobility [reports](https://www.google.com/covid19/mobility/) are now available at:
- [world dataset](/mobility/world.json.gz): countries + regions
- [US dataset](/mobility/us.json.gz): states + counties

For gzipped csv datasets:
- [world csv dataset](/mobility/world.csv.gz)
- [US csv dataset](/mobility/us.csv.gz)

An viz is also available [here](/mobility/charts/map.html).

Note that numbers for a whole country are available as a region, when the `region` column equals `total` (I hope no country has a region called `totals` !)

Thanks to reddit user _typhoidisbad_ who made this possible by [sharing](https://www.reddit.com/r/datasets/comments/fuo64p/google_covid19_mobility_reports_time_series_data/) his code, to produce the dataset on US states and counties.

Full source code and website is available [here](https://github.com/horaceg/covid19-analysis).  
Check out the `mobility` folder for this specific work.

Basic visualisations of this dataset can be found [here](https://github.com/horaceg/covid19-analysis/blob/master/mobility/viz.ipynb).

If you have any suggestion, please file an issue [here](https://github.com/horaceg/covid19-analysis/issues).

If you are looking for a general-purpose dashboard on Covid-19, check [this](/posts/covid-outbreak) out.
