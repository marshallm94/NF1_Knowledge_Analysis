import pandas as pd
import numpy as np
from collections import Counter


def grade_quiz(grand_data_filepath, answer_key_filepath):

    df = pd.read_csv(grand_data_filepath)
    answers = pd.read_csv(answer_key_filepath)

    quiz_columns = answers.question.unique()

    quiz_df = df[quiz_columns].copy()

    answers_liz = answers.to_dict(orient='records')

    graded_quiz = pd.DataFrame()
    for sub_dict in answers_liz:

        column_name = sub_dict['question']
        correct_answer = sub_dict['correct_answer']

        if correct_answer == 'True':

            correct_answer = 1
            graded_quiz[column_name] = np.where(quiz_df[column_name] == correct_answer, 1, 0)


        elif correct_answer == 'False':

            correct_answer = 0
            graded_quiz[column_name] = np.where(quiz_df[column_name] == correct_answer, 1, 0)

        elif correct_answer != 'True' or correct_answer != 'False':

            graded_quiz[column_name] = np.where(quiz_df[column_name] == correct_answer, 1, 0)

    graded_quiz['number_correct'] = graded_quiz.sum(axis=1)
    graded_quiz['total_quiz_questions'] = len(quiz_columns)
    graded_quiz['score'] = graded_quiz.number_correct / graded_quiz.total_quiz_questions

    demographic_cols = ['respondent_id',
                        'age',
                        'gender',
                        'ethnicity',
                        'educational_background',
                        'employment_status',
                        'do_you_have_nf1?',
                        "does_your_childs_other_parent_have_nf1?",
                        "have_you_ever_met_with_a_genetic_counselor?",
                        "Does your oldest child see a Neurologist for NF care?",
                        "Does your oldest child see an Oncologist for NF care?",
                        "Does your oldest child see a Geneticist for NF care?",
                        "Does your oldest child see an ENT/Audiologist for NF care?",
                        "Does your oldest child see a Pediatrician for NF care?",
                        "Does your oldest child see a Dermatologist for NF care?",
                        "Does your oldest child see a different doctor/specialist for NF care? (please specify)",
                        "How often does your (oldest) child see an NF doctor?",
                        "How would you describe the severity of symptoms of your (oldest) child with NF1?",
                        "If you have questions regarding NF1, do you obtain knowledge from your doctor?",
                        "If you have questions regarding NF1, do you obtain knowledge from family members with NF1?",
                        "If you have questions regarding NF1, do you obtain knowledge from online searches?",
                        "If you have questions regarding NF1, do you obtain knowledge from an NF organization website?",
                        "If you have questions regarding NF1, do you obtain knowledge from social media sites (such as Facebook)?",
                        "If you have questions regarding NF1, do you obtain knowledge from other families you know that have NF1?",
                        "Do you not have any questions regarding NF1?",
                        "If you have questions regarding NF1, do you not obtain additional information?",
                        "If you have questions regarding NF1, do you obtain knowledge from other sources? (please specify)"]

    updated_cols = []
    for col in demographic_cols:
        updated_cols.append(col.replace(" ","_").replace(',','').lower())

    for col in updated_cols:
        graded_quiz[col] = df[col].copy()

    updated_cols.append('score')
    updated_cols.extend(quiz_columns)    
    return graded_quiz[updated_cols].copy()


def create_genetic_groups(df, group_colname='group_id'):

    df_copy = df.copy()

    mask_a1 = df_copy['does_your_childs_other_parent_have_nf1?'] == "No"
    mask_a2 = df_copy['do_you_have_nf1?'] == "No"

    mask_b1 = df_copy['does_your_childs_other_parent_have_nf1?'] == "Yes"
    mask_b2 = df_copy['do_you_have_nf1?'] == "No"

    df_copy.loc[mask_a1 & mask_a2, group_colname] = 'Group A'
    df_copy.loc[mask_b1 & mask_b2, group_colname] = 'Group B'
    df_copy.loc[pd.isna(df_copy[group_colname]), group_colname] = "Group C"

    return df_copy


def create_groups(df, group_colname="have_you_ever_met_with_a_genetic_counselor?"):

    df_copy = df.copy()

    mask = df_copy[group_colname] == "Not sure"

    df_copy.loc[mask, group_colname] = "No"

    return df_copy


if __name__ == "__main__":

    df = grade_quiz("../data/grand_data_updated.csv", "../data/grand_data_answer_key_updated.csv")

    # drop 11 people who aren't sure if they have nf1
    df = df[df['do_you_have_nf1?'] != "Not sure"].copy()

    df[(df['does_your_childs_other_parent_have_nf1?'] == 'Yes') & (df['do_you_have_nf1?'] == "No")]

    mask = pd.isna(df['does_your_childs_other_parent_have_nf1?'])

    df.loc[mask, "does_your_childs_other_parent_have_nf1?"] = "No"

    # drop person who skipped 'do you have nf1' question
    df.drop(266, axis=0, inplace=True)

    # dropping participants who do not have nf1 and are not sure if other parent has nf1
    not_sure_idx = df[(df["does_your_childs_other_parent_have_nf1?"] == "Not sure") & (df['do_you_have_nf1?'] == "No")].index

    df.drop(not_sure_idx, axis=0, inplace=True)

    # dropping two participants who didn't answer below question
    no_answer_idx = df.loc[pd.isna(df['how_often_does_your_(oldest)_child_see_an_nf_doctor?'])].index
    df.drop(no_answer_idx, axis=0, inplace=True)

    # dropping one person who didn't answer below question
    df.drop(df.loc[pd.isna(df['how_would_you_describe_the_severity_of_symptoms_of_your_(oldest)_child_with_nf1?']),:].index, axis=0, inplace=True)

    df = create_genetic_groups(df)

    df = create_groups(df)

    df.to_csv("../data/grand_data.csv", index=False)
