import pandas as pd
from fuzzywuzzy import fuzz
import numpy as np
# import seaborn as sns
# import matplotlib.pyplot as plt

# # Define the input text and comparison texts
# input_text = ["Bhibhas Singh, luknow, F:Akhilesh Kumar Singh"]
# compare_texts = [["Vibhas Kumar Singh, Lucknow F: Akhilesh Singh"],
# ["Bibhas  Singh, Lucknow, F: Akhilesh Singh Yadav"],
# ["Vibhas Singh F: Akhilesh Kumar Lucknow"]]

# Calculate similarity between input text and comparison texts using fuzzy logic
def find_similar_texts_fuzzy(input_text, compare_texts, threshold=10):
    similarities = []
    for i in range(len(input_text)):
        for j in range(len(compare_texts)):
            sim = fuzz.ratio(input_text[i], compare_texts[j])
            if sim > threshold:
                similarities.append((input_text[i], compare_texts[j], sim))
    return similarities

# Find similar texts using fuzzy logic

# def final_similar(input_text, compare_texts):
#     similarities_fuzzy = find_similar_texts_fuzzy(input_text, compare_texts, threshold=10)
#     print(similarities_fuzzy)
#
#     # Create a confusion matrix
#     confusion_matrix = np.zeros((len(input_text), len(compare_texts)))
#
#     #for scoring  block
#     for pair in similarities_fuzzy:
#         input_txt, compare_txt, sim = pair
#         i = input_text.index(input_txt)
#         j = compare_texts.index(compare_txt)
#         confusion_matrix[i][j] = sim
#
#     # Plot the confusion matrix
#     # plt.figure(figsize=(10, 8))
#     # sns.heatmap(confusion_matrix, annot=True, cmap='coolwarm', xticklabels=input_text, yticklabels=compare_texts)
#     # plt.title('Confusion Matrix of Similarities')
#     # plt.show()
#
#     # Display final similar texts with score
#     print("\nFinal similar texts with score:")
#     for pair in similarities_fuzzy:
#         input_txt, compare_txt, sim = pair
#         print(f"Input text '{input_txt}' is similar to Compare text '{compare_txt}' with similarity: {sim:.2f}")
#
#     return "Done"

#final_similar(input_text, compare_texts)