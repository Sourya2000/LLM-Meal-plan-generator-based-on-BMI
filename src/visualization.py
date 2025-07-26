import fitz  # PyMuPDF
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import re

# Load PDF and extract text
pdf_path = "C:\\Users\\AMS\\Downloads\\Contact Information (Responses) - Form responses 1.pdf"
doc = fitz.open(pdf_path)
text = ""
for page in doc:
    text += page.get_text()

# Split text into lines and extract Rating and Comment
lines = text.split('\n')
data = []

for line in lines:
    match = re.search(r'(?P<comment>.*?)(?=\s+)?(?P<rating>[1-5])\s*$', line)
    if match:
        comment = match.group("comment").strip()
        rating = int(match.group("rating"))
        
        # Clean comment: remove emails and phone numbers
        comment = re.sub(r'\S+@\S+', '', comment)  # remove emails
        comment = re.sub(r'\b\d{10}\b', '', comment)  # remove 10-digit phone numbers
        comment = re.sub(r'\d{5,}', '', comment)  # remove any 5+ digit numbers
        comment = comment.strip(" -–")

        data.append({"Rating": rating, "Comments": comment})

# Create DataFrame
df = pd.DataFrame(data)

# Pie Chart for Ratings
rating_counts = df["Rating"].value_counts().sort_index()
plt.figure(figsize=(6, 6))
plt.pie(rating_counts, labels=rating_counts.index, autopct='%1.1f%%', startangle=140)
plt.title("Rating Distribution")
plt.axis("equal")
plt.tight_layout()
plt.savefig("rating_pie_chart.png")
plt.show()

# WordCloud for Cleaned Comments
comments_text = " ".join(comment for comment in df["Comments"] if comment.strip())
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(comments_text)

plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.tight_layout()
plt.savefig("comments_wordcloud.png")
plt.show()
