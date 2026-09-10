import pandas as pd

df = pd.read_csv(r'C:\Users\vysha\OneDrive\Desktop\prognosx\data\processed\final_dataset\training_manifest_labeled.csv')

pathologies = ['Atelectasis', 'Cardiomegaly', 'Consolidation', 'Edema',
               'Enlarged Cardiomediastinum', 'Fracture', 'Lung Lesion',
               'Lung Opacity', 'No Finding', 'Pleural Effusion',
               'Pleural Other', 'Pneumonia', 'Pneumothorax', 'Support Devices']

print("Missing (blank) values per pathology:")
print(df[pathologies].isna().sum())
print()
print("Value counts per pathology (1=positive, 0=negative, -1=uncertain):")
print(df[pathologies].apply(pd.Series.value_counts))