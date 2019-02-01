import pandas as pd
import numpy as np


def count_nans(df, columns, verbose=True):
    """
    Calculates nan value percentages per column in a pandas DataFrame.

    Parameters:
    ----------
    df : (Pandas DataFrame)
    columns : (list)
        A list of strings of the columns to check for null values. Note
        that even if you are checking only one column, it must be
        contained within a list. (Pass df.columns to check all columns)
    verbose : (bool)
        If True (default), prints column names and NaN percentage

    Returns:
    ----------
    col_nans : (list)
        List containing tuples of column names and percentage NaN for
        that column.
    """
    col_nans = []
    for col in columns:
        percent_nan = pd.isna(df[col]).sum()/len(pd.isna(df[col]))
        col_nans.append((col, percent_nan))
        if verbose:
            print("{} | {:.2f}% NaN".format(col, percent_nan*100))

    return col_nans


def clean_age_of_diagnosis_column(df, column='diagnosis_age_updated'):

    df_copy = df.copy()

    mask = df_copy[column].str.contains('month', case=False, na=False)
    mask2 = df_copy[column].str.contains('mos', case=False, na=False)

    df_copy.loc[mask | mask2, 'age_of_diagnosis'] = df_copy.loc[mask | mask2, column].str.extract('(\d+)', expand=False).astype(int) / 12

    df_copy.loc[~(mask | mask2), 'age_of_diagnosis'] = df_copy.loc[~(mask | mask2), column]


    week_mask = df_copy[column].str.contains('week', case=False, na=False)

    df_copy.loc[week_mask, 'age_of_diagnosis'] = df_copy.loc[week_mask, column].str.extract('(\d+)', expand=False).astype(int) / 52

    df_copy.age_of_diagnosis = df_copy.age_of_diagnosis.astype(float)

    df_copy.drop(column, inplace=True, axis=1)

    return df_copy


def clean_age_column(df, column='at_what_age_were_you_diagnosed_with_nf1?'):

    df_copy = df.copy()

    mask = df_copy[column].str.contains('birth',case=False, na=False)

    df_copy.loc[mask, column] = 0

    # manually setting
    df_copy.loc[37, column] = 7
    df_copy.loc[61, column] = 1
    df_copy.loc[61, column] = 1
    df_copy.loc[81, column] = float(1/12)
    df_copy.loc[129, column] = 0
    df_copy.loc[149, column] = "Unknown"
    df_copy.loc[152, column] = float(5/12)
    df_copy.loc[153, column] = 0
    df_copy.loc[165, column] = 4
    # setting to same as his/her answer in age column
    df_copy.loc[179, column] = 29
    df_copy.loc[197, column] = 5
    df_copy.loc[201, column] = "Unknown"
    # his/her mom knew when he/she was born therefore setting to birth/0
    df_copy.loc[207, column] = 0
    df_copy.loc[213, column] = float(7/12)
    # setting to 10 since he/she said 10 or 12
    df_copy.loc[231, column] = 10
    df_copy.loc[234, column] = "Unknown"
    df_copy.loc[239, column] = 4
    df_copy.loc[278, column] = "Unknown"
    df_copy.loc[298, column] = 12

    return df_copy




def convert_to_binary(df, columns):

    df_copy = df.copy()

    for column in columns:

        nan_mask = df_copy[column].isna()

        df_copy.loc[nan_mask, column] = 0
        df_copy.loc[~nan_mask, column] = 1

    return df_copy


def convert_binary_quiz_question(df, columns):

    df_copy = df.copy()

    for column in columns:

        df_copy[column] = np.where(df_copy[column] == True, 1, 0)

    return df_copy


def clean_data(filepath, updated_filepath):

    df = pd.read_excel(filepath)

    columns = [col.lower().replace(" ", "_") for col in df.columns]
    df.columns = columns

    df = clean_age_of_diagnosis_column(df)

    df = clean_age_column(df)

    to_binary_columns = ['does_your_oldest_child_see_a_neurologist_for_nf_care?',
         'does_your_oldest_child_see_an_oncologist_for_nf_care?',
         'does_your_oldest_child_see_a_geneticist_for_nf_care?',
         'does_your_oldest_child_see_an_ent/audiologist_for_nf_care?',
         'does_your_oldest_child_see_a_pediatrician_for_nf_care?',
         'does_your_oldest_child_see_a_dermatologist_for_nf_care?',
         'did_you_meet_with_a_genetic_counselor_during_initial_diagnostic_evaluation?',
         'did_you_meet_with_a_genetic_counselor_after_your_diagnosis_of_nf1?',
         'did_you_meet_with_a_genetic_counselor_at_follow_up_visits?',
         'did_you_meet_with_a_genetic_counselor_before_or_during_pregnancy_of_oldest_affected_child?',
         'did_you_meet_with_a_genetic_counselor_before_or_during_pregnancy_of_subsequent_children?',
         'did_a_doctor_explain_the_medial_aspects_of_nf1_to_you?',
         'did_a_genetic_counselor_explain_the_medial_aspects_of_nf1_to_you?',
         'did_a_family_member_explain_the_medial_aspects_of_nf1_to_you?',
         'did_no_one_explain_the_medial_aspects_of_nf1_to_you?',
         'are_you_not_sure_who_explained_the_medial_aspects_of_nf1_to_you?',
         'if_you_have_questions_regarding_nf1,_do_you_obtain_knowledge_from_your_doctor?',
         'if_you_have_questions_regarding_nf1,_do_you_obtain_knowledge_from_family_members_with_nf1?',
         'if_you_have_questions_regarding_nf1,_do_you_obtain_knowledge_from_online_searches?',
         'if_you_have_questions_regarding_nf1,_do_you_obtain_knowledge_from_an_nf_organization_website?',
         'if_you_have_questions_regarding_nf1,_do_you_obtain_knowledge_from_social_media_sites_(such_as_facebook)?',
         'if_you_have_questions_regarding_nf1,_do_you_obtain_knowledge_from_other_families_you_know_that_have_nf1?',
         'do_you_not_have_any_questions_regarding_nf1?',
         'if_you_have_questions_regarding_nf1,_do_you_not_obtain_additional_information?',
         'is_scoliosis_associated_with_nf1?',
         'is_attention_deficit_hyperactivity_disorder_associated_with_nf1?',
         'are_clubbed_feet_associated_with_nf1?',
         'are_congenital_heart_defects_associated_with_nf1?',
         'are_seizures_associated_with_nf1?',
         'are_bumps_on_the_skin_associated_with_nf1?',
         'are_allergies_associated_with_nf1?',
         'is_high_blood_pressure_associated_with_nf1?',
         'are_learning_disabilities_associated_with_nf1?',
         'are_optic_gliomas_associated_with_nf1?',
         'is_infertility_associated_with_nf1?',
         'are_lisch_nodules_(dark_spots_on_the_iris;_the_colored_part_of_the_eye)_associated_with_nf1?',
         'is_small_head_size_associated_with_nf1?',
         'are_cataracts_associated_with_nf1?']

    df = convert_to_binary(df, to_binary_columns)

    binary_quiz_questions = ['one_half,_or_50%,_of_genetic_information_is_passed_down_from_mother_to_child.',
         'there_is_more_than_one_gene_that_causes_nf1.',
         'a_father_can_pass_down_an_nf1_gene_mutation_to_his_daughters.',
         'all_people_who_have_an_nf1_gene_mutation_will_develop_cancer.',
         'nf1_symptoms_vary_from_one_person_to_another.',
         'a_person_is_born_with_nf1.',
         'nf1_can_skip_generations.',
         'if_a_woman_with_nf1_has_one_child_with_nf1,_her_second_child_will_definitely_not_have_nf1.',
         'people_with_nf1_are_generally_more_likely_to_develop_cancer_at_a_younger_age.',
         'if_a_woman_with_nf1_has_scoliosis,_then_her_child_will_also_develop_scoliosis.',
         'tumors_in_nf1_can_appear_anywhere_in_the_body.',
         'people_with_nf1_from_different_families_will_always_have_different_symptoms.',
         'if_a_woman_with_nf1_has_scoliosis,_then_her_child_will_also_develop_scoliosis.',
         'tumors_in_nf1_can_appear_anywhere_in_the_body.',
         'people_with_nf1_from_different_families_will_always_have_different_symptoms.',
         'cafe-au-lait_spots_(brown_marks_on_the_skin)_are_often_the_first_sign_that_a_person_has_nf1.',
         'a_baby_with_nf1_may_be_born_with_a_tumor.',
         "all_cases_of_nf1_can_be_detected_in_a_woman's_pregnancy_by_ultrasound.",
         'half_of_people_with_nf1_have_a_family_history_of_nf1.',
         'a_person_with_nf1_can_develop_tumors_that_may_lead_to_vision_loss_or_blindness.',
         'women_with_nf1_are_at_an_increased_risk_for_breast_cancer.']

    df = convert_binary_quiz_question(df, binary_quiz_questions)

    columns = [col.replace(",","") for col in df.columns]
    columns = [col.replace(".","") for col in columns]
    columns = [col.strip() for col in columns]
    columns = [col.replace("'","") for col in columns]
    df.columns = columns

    df.to_csv(updated_filepath, index=False)

    return df


def clean_answerkey(filepath, updated_filepath):

    df = pd.read_excel(filepath)

    new_columns = [col.lower().replace(" ", "_") for col in df.columns]
    df.columns = new_columns

    df.question = df.question.str.replace(" ", "_")
    df.question = df.question.str.replace(",", "")
    df.question = df.question.str.lower()
    df.question = df.question.str.strip()
    df.question = df.question.str.replace(".","")
    df.question = df.question.str.replace("'","")

    df.iloc[37, 1] = 1

    df.to_csv(updated_filepath, index=False)


if __name__ == "__main__":

    test = clean_data("../data/grand_data.xlsx", "../data/grand_data_updated.csv")

    clean_answerkey("../data/grand_data_answer_key.xlsx", "../data/grand_data_answer_key_updated.csv")
