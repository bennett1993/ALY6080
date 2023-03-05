import pandas as pd
pd.set_option('display.max_columns', 500)
from pathlib import Path
import os
import glob
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(font_scale=1.5)
import nbconvert
import numpy as np
import scipy
import statsmodels.formula.api as smf
import statsmodels.api as sm
import warnings
warnings.filterwarnings('ignore')
import streamlit as st
from datetime import date as dt
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
from keybert import KeyBERT
from PIL import Image

st.set_page_config(page_title='EDA', layout="centered")
st.sidebar.header('EDA')

header = st.container()
exec_summary = st.container()
business_prob = st.container()
datasets = st.container()
eda = st.container()
preprocessing = st.container()
models_considered = st.container()
models = st.container()
recommendations = st.container()
future_research = st.container()
other_relevant = st.container()
citations = st.container()

st.markdown(
    """
    <style>
    .main{
    background-color: #F5F5F5
    }
    </style>
    """,
    unsafe_allow_html=True
)

@st.cache_data()
def get_datasets():
    new_resulting_factors = pd.read_csv("https://raw.githubusercontent.com/bennett1993/ALY6080/main/new_resulting_factors.csv")
    patient_info = pd.read_csv("https://raw.githubusercontent.com/bennett1993/ALY6080/main/patient_info.csv")
    word_banks = pd.read_csv("https://raw.githubusercontent.com/bennett1993/ALY6080/main/word_banks.csv")
        
    return new_resulting_factors, patient_info, word_banks
    

with datasets:
    new_resulting_factors, patient_info, word_banks = get_datasets()  

with eda:
    st.header('Exploratory Data Analysis')
    
    first_chart = st.slider('Please choose the number of factors that you would like to see', min_value=1, max_value=20, value=10, step=1)
    
    fig = plt.figure(figsize=(16, 8))
    ax = sns.countplot(x="factor", data = new_resulting_factors, order=pd.value_counts(new_resulting_factors['factor']).iloc[:first_chart].index)
    plt.xticks(rotation=90)
    plt.title('Top f"{}" Factor Frequencies')
    
    for p in ax.patches:
        height = p.get_height()
        ax.text(x = p.get_x()+(p.get_width()/2), 
        y = height+80, 
        s = '{:.0f}'.format(height), 
        ha = 'center')
 
    st.pyplot(fig)
    
    second_chart = st.radio('Would you like the following chart in ascending or descending order?',('Ascending', 'Descending'))
    color = st.color_picker('Pick a color for the following chart', '#00f900')
    
    if second_chart == 'Ascending':
        second_chart = True
    elif second_chart == 'Descending':
        second_chart = False
    
    fig = plt.figure(figsize=(16, 8))
    ax = sns.countplot(x='subcategory', data = new_resulting_factors, order=new_resulting_factors['subcategory'].value_counts(ascending=second_chart).index,color=color)
    plt.xticks(rotation=90)
    plt.title('Subcategory Frequencies')
    
    for p in ax.patches:
        height = p.get_height()
        ax.text(x = p.get_x()+(p.get_width()/2), 
        y = height+100, 
        s = '{:.0f}'.format(height), 
        ha = 'center') 
        
    st.pyplot(fig)
    
    third_chart = st.slider('Please choose the number of patients that you would like to see', min_value=1, max_value=20, value=10, step=1)
    df = new_resulting_factors.groupby('patient_id').size().reset_index(name='number_entries')
    df = df.sort_values(by='number_entries',ascending=False)
    d = dict([(y,x+1) for x,y in enumerate(sorted(set(df['patient_id'])))])
    df['patient_id']= df['patient_id'].map(d)
    df = df.iloc[:third_chart]
    
    fig = plt.figure(figsize=(16, 8))
    ax = sns.barplot(x = 'patient_id', y = 'number_entries', data=df, order=df.sort_values('number_entries',ascending = False).patient_id)
    plt.title('Subcategory Frequencies')
    
    for p in ax.patches:
        height = p.get_height()
        ax.text(x = p.get_x()+(p.get_width()/2), 
        y = height+100, 
        s = '{:.0f}'.format(height), 
        ha = 'center') 
        
    st.pyplot(fig)
    
    fig = plt.figure(figsize=(10, 5))    
    df = patient_info.groupby(by='gender').size().reset_index(name='count')
    df = df.sort_values(by='count')
    
    color1 = st.color_picker('Pick your first color for the pie chart', '#00f900')
    color2 = st.color_picker('Pick your second color for the pie chart', "#4CAF50")
    color3 = st.color_picker('Pick your third color for the pie chart', '#FFC0CB')
    mycolors = [color1, color2, color3]
    plt.pie(df['count'],labels=df['gender'],autopct='%1.2f%%', colors = mycolors)
    plt.title("Gender Frequencies")
    
    st.pyplot(fig) 

with preprocessing:
    st.header('Preprocessing Steps')
    
    image = Image.open('image8.png')
    st.image(image, caption='(Baheti, 2023)')
    
    st.markdown(
        """
        - Data Prep
            - Patient id's from all four dataframes were stacked on top of each other, then only unique patient id's were kept and stored in dataframe df1
            - Data used was the note column of additional_notes, description column of new_resulting_factors, factor column of registered_factors, and describe_event column of tbi_incident 
            - The four dataframes were grouped on patient_id, unique patient_id was determined, and then strings for each unique patient_id were combined with a space in between
            - New additional_notes was merged to df1 on patient_id to create master_data dataframe
            - Other three dataframes were merged with master_data on patient_id
            - Null and TRUE values in master_data were replaced with empty strings, all strings made lowercase, and stop words removed
        """)

with models_considered:
    st.header('Models Considered')
    image1 = Image.open('image9.jpeg')
    st.image(image1, caption='(Mall, 2021)')
    image2 = Image.open('image10.png')
    st.image(image2, caption='(Chenery-Howes, 2022)')
    image3 = Image.open('image11.jpeg')
    st.image(image3, caption='(Zhu et al., 2021)')
    
    st.markdown(
        """
        - LDA and LSI:
            - Pros:
                - Models are simple and easy to understand
                - Models are fast and can quickly mine text data
            - Cons:
                - Word banks were trivial and did not offer useful results
        - BERT:
            - Pros:
                - Model created meaningful word banks
                - BERT is a transformer model which is a neural network approach to NLP
                - Pretrained model using large data sets
            - Cons:
                - Black-Box model
                - Computationally expensive
        """)

with models:
    st.header('Model Training Time!')
    
    st.write('Please consult the following link for the KeyBERT extract_keywords function parameters: https://maartengr.github.io/KeyBERT/api/keybert.html#keybert._model.KeyBERT.extract_keywords')
    
    a = st.slider('Choose the upper bound for the number of words in each phrase', min_value=1, max_value=3, value=1, step=1)
    b = st.slider('Choose the number of keywords and phrases you would like', min_value=4, max_value=5, value=4, step=1)
    c = st.select_slider('Would you like to use Max Sum Distance for the determination of keywords and phrases?', options=['Yes', 'No Thank You'])
    
    if c == 'Yes':
        c = True
    elif c == 'No Thank You':
        c = False
        
    d = st.select_slider('Would you like to use Maximal Marginal Relevance (MMR) for the determination of keywords and phrases?', options=['Yes', 'No Thank You'])
    
    if d == 'Yes':
        d = True
    elif d == 'No Thank You':
        d = False
        
    e = st.slider('If you are using MMR, please choose the diversity of the keyword/keyphrase results:', min_value=0.0, max_value=1.0, value=0.0, step=0.1)
    f = st.slider('If you are using Max Sum Distance, please choose the number of candidates to examine:', min_value=15, max_value=20, value=15, step=5)
    
    st.write('Here are your word banks for the chosen parameters:')
    
    word_banks[['patient_id', f"{a}_{b}_{c}_{d}_{e}_{f}"]]
    
    options = st.multiselect('Would you like to get word banks for specific patients?',word_banks['patient_id'])
    
    filtered_df = word_banks[word_banks['patient_id'].isin(options)]
    
    if options:
        filtered_df[['patient_id', f"{a}_{b}_{c}_{d}_{e}_{f}"]]
    else:
        word_banks[['patient_id', f"{a}_{b}_{c}_{d}_{e}_{f}"]]

with recommendations:
    st.header('Recommendations and Findings')
    
    image4 = Image.open('image12.png')
    st.image(image4, caption='(“Sentiment Classification,” 2021)')
    
    st.markdown(
        """
        - The BERT model is the optimal model and is recommended
            - The BERT topic model can be used to extract the top N keywords
            - These words can be combined to design a word bank
        - Model Best Practices:
            - Word bank quality is higher with more notes offered by the patients
            - Model should be ran as needed when new patients are added to the system
        """)
    
with future_research:
    st.header('Future Research')
    st.markdown(
        """
        - Sentiment analysis using the word banks
            - Retain historical word banks as the model is re-ran
            - Use sentiment analysis to understand if the emotion of the patients is changing over time
        - Enhancing user experience of Streamlit application
            - Adding more user inputs
            - Adding to visual appeal
        """)
    
with other_relevant:
    st.header('Other Relevant Information')
    
    image5 = Image.open('image13.jpeg')
    st.image(image5, caption='(“Phone Repair,” n.d.)')
    image6 = Image.open('image14.jpeg')
    st.image(image6, caption='(Sullivan, 2020)')
    
    st.markdown(
        """
        - Possible avenues to explore:
            - Phone, watch, and wearable applications for convenient data entry
            - Fingerprint or face login because users often forget their passwords
            - Voice to text in symptom tracker
            - Determining patient emotion from voice
            - Word banks by symptom - common words and phrases used to describe given symptoms
            - Identify commonalities among patients in different groups (gender, age, etc.)
        """)
    
with citations:
    st.header('Citations')
    st.markdown(
        """
        1. Baheti, P. (2023, February 2). A Simple Guide to Data Preprocessing in Machine Learning. V7. https://www.v7labs.com/blog/data-preprocessing-guide
        2. Chenery-Howes, A. (2022, December 21). What Is Latent Semantic Indexing And How Does It Works? Oncrawl - Technical SEO Data. https://www.oncrawl.com/technical-seo/what-is-latent-semantic-indexing/
        3. Grootendorst, M. P. (n.d.). KeyBERT - KeyBERT. https://maartengr.github.io/KeyBERT/api/keybert.html
        4. Mall, R. (2021, December 7). Latent Dirichlet Allocation - Towards Data Science. Medium. https://towardsdatascience.com/latent-dirichlet-allocation-15800c852699
        5. Phone Repair. (n.d.). iFixit. https://www.ifixit.com/Device/Phone
        6. Sentiment Classification Using BERT. (2021, September 8). GeeksforGeeks. https://www.geeksforgeeks.org/sentiment-classification-using-bert/
        7. Sullivan, F. &. (2020, September 29). Wearable Technologies and Healthcare: Differentiating the Toys and Tools for Quantified-Self' with Actionable Health Use Cases. Frost & Sullivan. https://www.frost.com/frost-perspectives/wearable-technologies-and-healthcare-differentiating-toys-and-tools-quantified-self-actionable-health-use-cases/
        8. Zhu, R., Tu, X., & Huang, J. X. (2021). Utilizing BERT for biomedical and clinical text mining. Data Analytics in Biomedical Engineering and Healthcare, 73-103. https://doi.org/10.1016/b978-0-12-819314-3.00005-7
        """)