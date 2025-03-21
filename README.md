# UFC_Stats

This is just a personal project. The goal here is just to learn and practice various tools and languages (which is why I might be doing things using "the wrong tools"), all the while making some hopefully cool and insightful vizualisations in Power BI and Excel PowerPivot.

The sources for the raw data are:

* fighters.json: https://github.com/victor-lillo/octagon-api/
* ufc-master.csv: https://www.kaggle.com/datasets/mdabbert/ultimate-ufc-dataset/data?select=ufc-master.csv

I process the fighters.json data using simple Python to convert it into a CSV that includes a fighter_id field. The ufc-master.csv is also missing a unique fight_id which I create in a SSIS task. An extra intermediary table is also created to transform a many-to-many connection in the data model into one-to-many connections. The data is then loaded into a SQL Server database, from which it's consumed by the Power BI and Excel PowerPivot reports. At least that's the plan.

Any suggestions on improvements are welcome, but only on already "feature-complete" parts, since my goal is to start by doing things by myself 🏻
