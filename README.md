# Challenge-2024-Metrics
2024 ISIC Challenge primary prizes and secondary prize scoring algorithms

### Primary Scoring Metric
For the leaderboard prizes, submissions are evaluated on **partial area under the ROC curve (pAUC)** above 88% true positive rate (TPR) for binary classification of malignant examples.

The receiver operating characteristic (ROC) curve illustrates the diagnostic ability of a given binary classifier system as its discrimination threshold is varied. However, there are regions in the ROC space where the values of TPR are unacceptable in clinical practice. Systems that aid in diagnosing cancers are required to be highly-specific, so this metric focuses on the area under the ROC curve AND above 88% TRP. Therefore, scores range from [0.00, 0.12].

The shaded regions in the following figure represents the pAUC of two algorithms:

![Jiang](https://github.com/ISIC-Research/Challenge-2024-Metrics/assets/33763338/314e75c5-1965-42d3-9dd7-384dd7c1d5c0)

### Seconary Scoring Metric
A secondary prize is awarded to the submission with the highest **top-15 retrieval sensitivity**.

