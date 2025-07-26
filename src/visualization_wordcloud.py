import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Read Excel file
df = pd.read_excel("C:\\Users\\AMS\hcai\\contact.xlsx")  # use raw string

# Replace 'comments' with the actual column name
text = ' '.join(df['Comments'].dropna().astype(str))

# Create and display WordCloud
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()
