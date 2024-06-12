# Challenge-2024-Metrics
2024 ISIC Challenge primary prizes and secondary prize scoring algorithms

## Primary Scoring Metric
For the leaderboard prizes, submissions are evaluated on **partial area under the ROC curve (pAUC)** above 88% true positive rate (TPR) for binary classification of malignant examples.

The receiver operating characteristic (ROC) curve illustrates the diagnostic ability of a given binary classifier system as its discrimination threshold is varied. However, there are regions in the ROC space where the values of TPR are unacceptable in clinical practice. Systems that aid in diagnosing cancers are required to be highly-specific, so this metric focuses on the area under the ROC curve AND above 88% TRP. Therefore, scores range from [0.00, 0.12].

The shaded regions in the following figure represents the pAUC of two algorithms:

![Jiang](https://github.com/ISIC-Research/Challenge-2024-Metrics/assets/33763338/314e75c5-1965-42d3-9dd7-384dd7c1d5c0)

## Two Secondary Scoring Metrics
- Top-15 retrieval sensitivity
- Model Efficiency

### Top-15 retrieval sensitivity
A secondary prize is awarded to the submission with the highest **top-15 retrieval sensitivity**.

Imagine you are a dermatologist conducting a full body skin exam for each patient that visits your clinic. Imagine that each patient undergoes 3D TBP prior to meeting you in the examination room. You have just a few minutes to spend with each patient, which is not enough time to view every lesion with your trusted dermatoscope. Wouldn't it be helpful if, by the time you walked into the room, an AI algorithm recommended a doable arbitrary number of each patient's most high-risk lesions to improve efficiency?

To help answer this question, one secondary prize will be awarded to the algorithm that is most successful in scoring malignancies within the top-15 highest scored images per patient. In the event of a tie, the algorithm that ranks the detected malignancies highest among those top-15 lesions per patient will win the secondary prize.

### Model Efficiency
Submissions will be evaluated for inference time on an undisclosed subset of test set images. This prize is optional and requires teams to submit a Kaggle notebook to the challenge organizers.
