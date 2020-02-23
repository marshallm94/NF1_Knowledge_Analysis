# NF1 Knowledge Analysis

[Statistical Analysis of NF1 Data](src/nf1_analysis.pdf)

To reproduce:

1. Run the [src/data_cleaning.py](src/data_cleaning.py) script.
	* This script cleans the data from the SurveyMonkey survey and
	transforms it into a more usable format for R.
		* [data/grand_data.xlsx](data/grand_data.xlsx) becomes [data/grand_data_updated.csv](data/grand_data_updated.csv).
	* The answer key (provided by the PI) was also cleaned to transform it
	into a a more usable format for R.
		* [data/grand_data_answer_key.xlsx](data/grand_data_answer_key.xlsx) becomes [data/grand_data_answer_key_updated.csv](data/grand_data_answer_key_updated.csv).

2. Run the [src/grade_quiz.py](src/grade_quiz.py) script.
	* This script grades the knowledge portion of the SurveyMonkey results,
	as well as removing some participants from the study (reasons for these
	removals can be found in the [analysis](src/nf1_analysis.pdf), as well
	as in comments in the Python script).

3. Knit nf1_analysis.Rmd (RStudio was the IDE used).

If you have any questions feel free to reach out to myself (marshallm94 at gmail dot com)
or the PI (emily dot p dot solem at vumc dot org).
