#!/bin/bash

# set -x
# https://www.google.com/covid19/mobility/

mkdir -p pdfs
cd pdfs

dates="2020-03-29 2020-04-05 2020-04-11"

country_codes="AD AE AF AG AI AL AM AO AR AT AU AW AZ BA BB BD BE BF BG BH BI BJ BLM BM BN BO BQ BR BS BT BW BY BZ CA CD CF CG CH CI CL CM CN CO CR CU CV CW CY CZ DE DJ DK DM DO DZ EC EE EG EL ER ES ET FI FJ FK FO FR GA GB GD GE GG GH GI GL GM GN GQ GR GT GU GW GY HK HN HR HT HU ID IE IL IM IN IQ IR IS IT JE JM JO JP JPG11668 KE KG KH KN KR KW KY KZ LA LB LC LI LK LR LT LU LV LY MA MC MD ME MG MK ML MM MN MP MR MS MT MU MV MW MX MY MZ NA NC NE NG NI NL NO NP NZ OM PA PE PF PG PH PK PL PR PS PT PY QA RE RO RS RU RW SA SC SD SE SG SI SK SL SM SN SO SR SV SX SY SZ TC TD TG TH TJ TL TN TR TT TW TZ UA UG UK US UY UZ VA VC VE VG VI VN XK YE ZA ZM ZW"
for date in $dates ; do
    mkdir -p $date
    cd $date
    for code in $country_codes ; do
        url=https://www.gstatic.com/covid19/mobility/${date}_${code}_Mobility_Report_en.pdf

        # Check if the status code is 200
        if curl -I 2>/dev/null $url | head -1 | grep 200 >/dev/null ; then
            curl -s -O $url
            echo downloaded $url
        fi
    done
    cd ..
done

cd ..
mkdir -p us_pdfs
cd us_pdfs

us_states="Alabama Alaska Arizona Arkansas California Colorado Connecticut Delaware District_of_Columbia Florida Georgia Hawaii Idaho Illinois Indiana Iowa Kansas Kentucky Louisiana Maine Maryland Massachusetts Michigan Minnesota Mississippi Missouri Montana Nebraska Nevada New_Hampshire New_Jersey New_Mexico New_York North_Carolina North_Dakota Ohio Oklahoma Oregon Pennsylvania Rhode_Island South_Carolina South_Dakota Tennessee Texas Utah Vermont Virginia Washington West_Virginia Wisconsin Wyoming"
for date in $dates ; do
    mkdir -p $date
    cd $date
    for state in $us_states ; do
        url=https://www.gstatic.com/covid19/mobility/${date}_US_${state}_Mobility_Report_en.pdf

        # Check if the status code is 200
        if curl -I 2>/dev/null $url | head -1 | grep 200 >/dev/null ; then
            curl -s -O $url
            echo downloaded $url
        fi
    done
    cd ..
done