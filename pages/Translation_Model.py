# import streamlit as st
# import pandas as pd
# import numpy as np
# from sentence_transformers import SentenceTransformer
# from sklearn.metrics.pairwise import cosine_similarity
# from googletrans import Translator

# # --- Constants ---
# MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"
# TOP_K = 30
# PKL_FILE = "paragraphs_with_embeddings_v2.pkl"
# SIMILARITY_THRESHOLD = 0.4


# # # --- UI Config ---
# # st.title("🔍 Multilingual Paragraph Search")
# # st.subheader("Built for PDF content in 2-column layout")

# # query = st.text_input("Enter a detailed query (minimum 5 words):")

# # # 👇 Add this slider to let user choose similarity threshold
# # threshold = st.slider(
# #     "Similarity Threshold (lower = more results, higher = more relevant)", 
# #     min_value=0.1, 
# #     max_value=0.9, 
# #     value=0.4, 
# #     step=0.05
# # )



# # --- Init ---
# @st.cache_resource
# def load_model():
#     return SentenceTransformer(MODEL_NAME)

# @st.cache_data
# def load_dataset():
#     return pd.read_pickle(PKL_FILE)

# model = load_model()
# translator = Translator()
# df = load_dataset()

# # --- App UI ---
# st.title("📄 Multilingual Paragraph Search")
# st.markdown("Search through multilingual technical documents, havng 2 column layout.")

# query = st.text_input("Enter search query (at least 6 words):")
# # translate_toggle = st.checkbox("🔁 Include translated paragraph (optional)", value=False)

# if st.button("🔍 Search"):

#     if not query or len(query.strip().split()) < 6:
#         st.warning("Please enter a search query with more than 5 words.")
#     else:
#         query_embedding = model.encode(query)
#         para_embeddings = np.vstack(df['embedding'].to_numpy())
#         scores = cosine_similarity([query_embedding], para_embeddings)[0]

#         df['score'] = scores
#         df_filtered = df[df['score'] >= SIMILARITY_THRESHOLD]
#         df_top = df_filtered.sort_values(by="score", ascending=False).head(TOP_K).copy()

#         if df_top.empty:
#             st.info("No matching paragraphs found.")
#         else:
#             st.success(f"Found {len(df_top)} matching paragraphs.")
            
#             # Optional Translation
#             # if translate_toggle:
#             #     df_top["translated_paragraph"] = df_top["paragraph"].apply(
#             #         lambda x: translator.translate(x, dest="en").text
#             #     )

#             # Display table
#             display_cols = ["doc_name", "page_number", "paragraph", "language", "score"]
#             # if translate_toggle:
#             #     display_cols.append("translated_paragraph")
#             st.dataframe(df_top[display_cols], use_container_width=True)

#             # Download
#             def convert_df_to_csv(df_export):
#                 return df_export.to_csv(index=False, encoding="utf-8-sig")

#             csv = convert_df_to_csv(df_top[display_cols])
#             st.download_button(
#                 label="📥 Download results as CSV",
#                 data=csv,
#                 file_name="filtered_paragraphs.csv",
#                 mime="text/csv"
#             )


#######################################################
#changed the script to pull model from another repo below 
#####################################################


import streamlit as st
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from googletrans import Translator
import os
import requests

# --- Constants ---
MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"
TOP_K = 30
PKL_URL = "https://raw.githubusercontent.com/mauryamanish1/translation_model/main/saved_models/paragraphs_with_embeddings_v2.pkl"
PKL_FILE = "paragraphs_with_embeddings_v2.pkl"
SIMILARITY_THRESHOLD = 0.4

# --- Download PKL if not present ---
def download_pickle_if_needed():
    if not os.path.exists(PKL_FILE):
        with st.spinner("Downloading paragraph data..."):
            try:
                r = requests.get(PKL_URL)
                r.raise_for_status()  # Raise an error for bad responses
                with open(PKL_FILE, "wb") as f:
                    f.write(r.content)
                st.success("Model file successfully downloaded!")
            except requests.exceptions.RequestException as e:
                st.error(f"Error downloading file: {e}")
                raise e
download_pickle_if_needed()

# --- Cached loaders ---
@st.cache_resource
def load_model():
    return SentenceTransformer(MODEL_NAME)

@st.cache_data
def load_dataset():
    # Load the dataset after checking it exists
    if not os.path.exists(PKL_FILE):
        download_pickle_if_needed()  # Ensure file is downloaded
    return pd.read_pickle(PKL_FILE)

# --- Load resources ---
model = load_model()
translator = Translator()
df = load_dataset()

# --- UI ---
st.title("🌐 Multilingual Paragraph Search")
st.markdown("Search technical documents with multilingual paragraphs (PDFs in 2-column layout).")

query = st.text_input("Enter a detailed search query (minimum 6 words):")
# Uncomment if translation is needed
# translate_toggle = st.checkbox("Include translated paragraph", value=False)

if st.button("🔍 Search"):
    if not query or len(query.strip().split()) < 6:
        st.warning("Please enter a query with more than 5 words.")
    else:
        query_embedding = model.encode(query)
        para_embeddings = np.vstack(df['embedding'].to_numpy())
        scores = cosine_similarity([query_embedding], para_embeddings)[0]
        df['score'] = scores

        df_filtered = df[df['score'] >= SIMILARITY_THRESHOLD]
        df_top = df_filtered.sort_values(by="score", ascending=False).head(TOP_K).copy()

        if df_top.empty:
            st.info("No matching paragraphs found.")
        else:
            st.success(f"Found {len(df_top)} matching paragraphs.")

            # Uncomment to translate
            # if translate_toggle:
            #     df_top["translated_paragraph"] = df_top["paragraph"].apply(
            #         lambda x: translator.translate(x, dest="en").text
            #     )

            display_cols = ["doc_name", "page_number", "paragraph", "language", "score"]
            # if translate_toggle:
            #     display_cols.append("translated_paragraph")

            st.dataframe(df_top[display_cols], use_container_width=True)

            def convert_df_to_csv(df_export):
                return df_export.to_csv(index=False, encoding="utf-8-sig")

            csv = convert_df_to_csv(df_top[display_cols])

            st.download_button(
                label="⬇️ Download results as CSV",
                data=csv,
                file_name="filtered_paragraphs.csv",
                mime="text/csv"
            )



