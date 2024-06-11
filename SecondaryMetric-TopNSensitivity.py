"""
patient_metric.py
-----------------

2024 ISIC Challenge patient-level (secondary) prize scoring algorithm

Reads in all submission CSVs from a given folder, and produces a
dataframe containing the average raw and weighted ranks of all
found true positives within the top-N scores per patient, sorted by
(1) raw average rank and (2) weighted average rank in descending
order, such that the winner is the submission with the highest
average rank (found malignancies weighted by patient), with ties
broken by algorithms finding those with relatively higher scores.

(c) 2024 Maura Gillis & Jochen Weber, MSKCC
"""

#Patient Metric Secondary Prize 
#This algorithm will start by looking for all submisssion files.

#IMPORTS 

import argparse
import glob 
import os 
import sys

import pandas as pd 
from tqdm import tqdm



def main():
    
    """
    patient_metric.py  main function

    will be called when module is run as __main__ (e.g. on the command line)
    """

    directory="Z:\\10.Imaging Informatics\\2024 ISIC Challenge\\Competition-metrics\\Patient Metric Submissions"


    parser = argparse.ArgumentParser(
        description="Evaluating multiple ISIC 2024 Challenge submissions on patient-level metric",
    )
    parser.add_argument("--directory", help="specifies the directory with the submission CSVs", default= "Z:\\10.Imaging Informatics\\2024 ISIC Challenge\\Competition-metrics\\Patient Metric Submissions")
    parser.add_argument("-c", "--column", help="column name with prediction scores", default="Predictions", type=str)
    parser.add_argument("-l", "--leaderboard", help="name of output leaderboard CSV file", default="leaders_patient_metric_2024.csv")
    parser.add_argument("-t", "--topn", help="include top N scores per patient", default=15, type=int)
    args = parser.parse_args()

    top_n = args.topn
    score_column = args.column

    # - define a directory 
    directory = args.directory

    if not os.path.exists(directory):
        raise ValueError("Missing or not-found directory.")
    leaderboard = args.leaderboard

    submissions=glob.glob(directory + "\\*.csv")
    no_submissions = len(submissions) #number of submissions

    print(f"Processing {no_submissions} submissions...")


    #Next, we will combine isic_id with the patient_ids and ground truth labels.
    

    ground_truth_folder = os.path.dirname(os.path.abspath(__file__))
    ground_truth=pd.read_csv(ground_truth_folder + os.path.sep + "test-gt.csv").set_index("isic_id")


    malignancies_per_patient = ground_truth.groupby('patient_id')['target'].sum().reset_index()

    number_of_malignancies=malignancies_per_patient['target'].sum()
    print(number_of_malignancies)



    #Filter ground truth by patients with at least one malignancy

    ground_truth=ground_truth[ground_truth.patient_id.isin(set(malignancies_per_patient[malignancies_per_patient.target > 0].patient_id))].copy()
    
    malignancies_per_patient = ground_truth.groupby('patient_id')['target'].transform('sum')


    ground_truth['target_fraction'] = ground_truth['target'].astype(float) / malignancies_per_patient


    average_ranks = [0.0] * no_submissions
    weighted_ranks = [0.0] * no_submissions
    sensitivity=[0.0]*no_submissions


    for index, submission in enumerate(tqdm(submissions)):

        data=pd.read_csv(submission).set_index("filenames")

        #Join with the patien_id, select the top n predictions grouped by patient_id. 

        data=data.join(ground_truth)
        data.head()

        data=data[~data.split.isna()]
        no_patients = len(set(data.patient_id))
        number_of_malignancies=data['target'].sum()

        
        # - Group by patient and select the top n probabilities

        top_values = data.groupby('patient_id', group_keys=False).apply(lambda x: x.nlargest(top_n, score_column)).reset_index()

        found_malignancies=top_values["target"].sum()

        not_found_malignancies=number_of_malignancies-found_malignancies

        sensitivity_calculation=found_malignancies/(found_malignancies+not_found_malignancies)

        sensitivity[index]=sensitivity_calculation

        
        top_values['rank'] = top_values.groupby('patient_id')[score_column].rank(method="dense") / float(top_n)
        top_values['weighted_fraction'] = top_values.target_fraction * top_values['rank']
        #print(top_values)

        raw_average_rank =top_values.target_fraction.sum() / no_patients
        weighted_average_rank =top_values.weighted_fraction.sum() / no_patients

        average_ranks[index]=raw_average_rank
        weighted_ranks[index]=weighted_average_rank
        


    #Sort submissions by total number of malignancies in decreasing order
    
    submission_scores = pd.DataFrame({
        "submissions":submissions,
        "average ranks":average_ranks,
        "weighted ranks": weighted_ranks,
        "sensitivity":sensitivity
    }).sort_values(by=["average ranks", "weighted ranks"], ascending=False).reset_index().drop('index', axis=1)
    print(submission_scores)

    submission_scores.to_csv(leaderboard, index=False)

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except:
        raise
