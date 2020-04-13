---
title: "Google mobility data"
date: 2020-04-04
draft: false
---

Last updated: **April 13 2020**

Google has recently published [mobility reports](https://www.google.com/covid19/mobility/), which essentially answer the question : _where do people spend their time ?_

They dispatch places into six categories : _workplace, residential, grocery & pharmacy, parks, retail & recreation, transit stations_.  
We are able to compare the current frequency at which these categories of places are visited _compared_ to a baseline, quoting Google reports:
> Changes for each day are compared to a baseline value for that day of the week. 

> The baseline is the median value, for the corresponding day of the week, during the 5-week period Jan 3–Feb 6, 2020


This allows us to evaluate quantitatively **social distancing**.  

I have made a synthetic [world visualization](/mobility/charts/map.html) of this data. 

Full timeseries data from the reports is also available here.  
Click on the links below to download the datasets in the csv format:
- [World csv dataset](/mobility/world.csv): countries + regions
- [US csv dataset](/mobility/us.csv): states + counties

Note that numbers for a whole country are available as a region, when the `region` column equals `total`

Thanks to reddit user _typhoidisbad_ who made this possible by [sharing](https://www.reddit.com/r/datasets/comments/fuo64p/google_covid19_mobility_reports_time_series_data/) his code, to produce the dataset on US states and counties.

Full source code and website is available [here](https://github.com/horaceg/covid19-analysis).  
Check out the `mobility` folder for this specific work.

If you have any suggestion, please file an issue [here](https://github.com/horaceg/covid19-analysis/issues).

If you are looking for a general-purpose dashboard on Covid-19, check [this](/posts/covid-outbreak) out.
