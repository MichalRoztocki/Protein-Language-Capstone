# Protein-Language-Capstone
FourthBrain Capstone: **Learning the Language of Proteins** (InstaDeep Industry Project)

Group Members: Damir, Michal, and Tikka

## Background (from InstaDeep)
Drug development and discovery is a time and labor intensive process that has the potential to be enhanced and improved by next-generation protein sequencing techniques.

Recent breakthroughs in Natural Language Processing (NLP) and training of large transformer models have paved the way for new types of domain-specific deep language models. In the biological domain, development of general-purpose protein language models that are capable of predicting specific protein types could, among other things, pave the way to more effective, safer cancer treatments.

## Tasks
A protein can be represented by a sequence of tokens where each token is an amino acid (e.g., GMASKAGSVLGKITKIALGAL). Peptides are proteins of relatively small lengths.

We have three datasets from InstaDeep, one for each of the following three classification tasks:
1. Anticancer Peptides (ACP) - develop a system that can predict, given a sequence of amino acids, if a peptide is an ACP or not
2. Antimicrobial Peptides (AMP) - develop a system that can predict, given a sequence of amino acids, if a peptide is an AMP or not
3. DNA-Binding Proteins (DBP) - develop a system that can predict, given a sequence of amino acids, if a peptide is a DBP or not

## Baseline Models
For each of the tasks listed above, we investigated two baseline models
1. Bag of Words (BoW) was used for sequence embedding, and then a simple Neural Network was used for classification
2. [Sequence Graph Transform (SGT)](https://github.com/cran2367/sgt) was used for sequence embedding, and then the same Neural Network was used for classification

Results are summarized below (Accuracy metric):
| Embedding   | Model         | ACP  |AMP   |DBP   |
| ----------- |:-------------:|-----:|-----:|-----:|
| BoW         | NN            | 68.1 |90.6  |79.1  |
| SGT         | NN            | 70.9 |82.5  |71.5  |

The BoW does not retain any sequence information. SGT uses the sequence information, but is not pre-trained on any protein data (it can handle any sequence data from scratch). It was rather surprising to see BoW do nearly as well (for ACP) or even better (for AMP and DBP).
