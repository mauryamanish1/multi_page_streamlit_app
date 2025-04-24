# import streamlit as st
# import fitz  # PyMuPDF
# from langdetect import detect
# from collections import Counter
# import pandas as pd
# import re
# import io
# from langdetect import detect
# import pycountry
# from langdetect import DetectorFactory

# #---------------------setting consistency------
# DetectorFactory.seed = 0



# # ---------------------- Helper Functions ----------------------

# def is_valid_paragraph(text):
#     text = text.strip()
#     if not text or len(text.split()) < 3:
#         return False

#     # Filter obvious noise
#     if re.match(r'^.*\.{4,}.*$', text):
#         return False

#     words = text.split()
#     word_count = len(words)
#     part_number_like = 0

#     for word in words:
#         cleaned = word.strip(".,;:()[]{}")
#         has_digits = any(char.isdigit() for char in cleaned)
#         long_enough = len(cleaned) > 3
#         if has_digits and long_enough:
#             part_number_like += 1

#     part_ratio = part_number_like / word_count if word_count else 0
#     if part_ratio > 0.3:
#         return False

#     has_punctuation = any(p in text for p in ['.', ':', ';', '!', '?'])
#     return has_punctuation



# def extract_text_by_columns(page, column_split=300):
#     blocks = page.get_text("blocks")
#     left_col, right_col = [], []
#     for b in blocks:
#         x0, y0, x1, y1, text, *_ = b
#         if x0 < column_split:
#             left_col.append((y0, text))
#         else:
#             right_col.append((y0, text))
#     left_col.sort()
#     right_col.sort()
#     combined_text = '\n'.join([t for _, t in left_col + right_col])
#     return combined_text

# def clean_line(line):
#     line = line.strip()
#     if not line or line.count('.') > 10:
#         return ''
#     if re.fullmatch(r'[-–—_\s\d.]+', line):
#         return ''
#     return line

# def extract_paragraphs_from_pdf(pdf_bytes, use_columns=True, column_split=300):
#     try:
#         doc = fitz.open(stream=pdf_bytes, filetype="pdf")
#     except Exception as e:
#         st.error("❌ Unable to read the PDF. Please check if it's a valid file.")
#         return []

#     paragraphs = []
#     for page_num, page in enumerate(doc, start=1):
#         text = extract_text_by_columns(page, column_split) if use_columns else page.get_text("text")
#         lines = [clean_line(line) for line in text.split('\n')]
#         lines = [line for line in lines if line]
#         para_buffer = ""
#         para_num = 0
#         for line in lines:
#             if para_buffer:
#                 para_buffer += ' ' + line.strip()
#             else:
#                 para_buffer = line.strip()
#             if re.search(r'[.?!:;]$', line.strip()) or len(line.strip()) < 40:
#                 if is_valid_paragraph(para_buffer):
#                     para_num += 1
#                     paragraphs.append({
#                         'page': page_num,
#                         'paragraph_number': para_num,
#                         'text': para_buffer.strip(),
#                         'word_count': len(para_buffer.strip().split())
#                     })
#                 para_buffer = ""
#         if is_valid_paragraph(para_buffer):
#             para_num += 1
#             paragraphs.append({
#                 'page': page_num,
#                 'paragraph_number': para_num,
#                 'text': para_buffer.strip(),
#                 'word_count': len(para_buffer.strip().split())
#             })
#     return paragraphs

# # def detect_languages(paragraphs):
# #     lang_results = []
# #     for p in paragraphs:
# #         try:
# #             lang = detect(p['text'])
# #         except Exception:
# #             lang = "unknown"
# #         p['language'] = lang
# #         lang_results.append(lang)
# #     return paragraphs, lang_results





# def get_language_name(code):
#     try:
#         return pycountry.languages.get(alpha_2=code).name
#     except:
#         return "Unknown"

# def detect_languages(paragraphs):
#     lang_results = []
#     for p in paragraphs:
#         try:
#             lang_code = detect(p['text'])
#             lang_name = get_language_name(lang_code)
#         except Exception:
#             lang_code = "unknown"
#             lang_name = "Unknown"
#         p['language'] = lang_name
#         lang_results.append(lang_name)
#     return paragraphs, lang_results




# def find_foreign_paragraphs(paragraphs, lang_results):
#     lang_count = Counter(lang_results)
#     if not lang_count:
#         return "unknown", []

#     major_language = lang_count.most_common(1)[0][0]
#     foreign_paragraphs = [
#         p for p in paragraphs if p['language'] != major_language and p['language'] != "unknown"
#     ]
#     return major_language, foreign_paragraphs

# def analyze_pdf_language_and_save_bytesio(pdf_bytes, file_name, use_columns=True, column_split=300):
#     paragraphs = extract_paragraphs_from_pdf(pdf_bytes, use_columns, column_split)
#     if not paragraphs:
#         return "unknown", pd.DataFrame(), b"", ""

#     paragraphs, lang_results = detect_languages(paragraphs)
#     major_language, foreign_paragraphs = find_foreign_paragraphs(paragraphs, lang_results)

#     if not foreign_paragraphs:
#         return major_language, pd.DataFrame(), b"", ""

#     df_foreign = pd.DataFrame(foreign_paragraphs)
#     clean_df_foreign = df_foreign.loc[df_foreign['word_count']>9]
#     output_csv = f"{file_name.replace('.pdf', '')}_foreign.csv"
#     csv_bytes = clean_df_foreign.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
#     return major_language, clean_df_foreign, csv_bytes, output_csv

# # ---------------------- Streamlit App ----------------------
# st.set_page_config(page_title="Foreign Language Detector", layout="centered")
# st.title("📄 Foreign Language Detector")

# uploaded_file = st.file_uploader("Upload a PDF file (<10 MB)", type=["pdf"])

# if uploaded_file is not None:
#     with st.spinner("Analyzing PDF..."):
#         try:
#             pdf_bytes = uploaded_file.read()
#             major_lang, df, csv_bytes, output_csv = analyze_pdf_language_and_save_bytesio(
#                 pdf_bytes, uploaded_file.name
#             )

#             if df.empty:
#                 st.warning("No foreign language paragraphs were detected.")
#             else:
#                 st.success(f"✅ Major language: {major_lang}")
#                 st.info(f"Found {len(df)} foreign paragraphs.")
#                 st.dataframe(df[['page', 'language', 'text']].head(10))
#                 st.download_button(
#                     label="⬇️ Download Foreign Paragraphs CSV",
#                     data=csv_bytes,
#                     file_name=output_csv,
#                     mime="text/csv"
#                 )
#         except Exception as e:
#             st.error(f"❌ An unexpected error occurred during analysis.")
#             st.exception(e)






################### v2 below #################


# %%
import streamlit as st
import fitz  # PyMuPDF
import pandas as pd
import time
from langdetect import detect, DetectorFactory
from collections import Counter
import re  # Import the 're' module
from googletrans import Translator, LANGUAGES

# Initialize Google Translator
translator = Translator()

# --- CONFIGURATION ---
DetectorFactory.seed = 0
MIN_PARAGRAPH_WORDS = 10
MAX_HEADING_WORDS = 10
TOC_LEFT_THRESHOLD_PERCENT = 0.1
MIN_ALPHA_RATIO_FOR_LANG_DETECTION = 0.4
COMMON_SPANISH_WORDS = set(['TRABAJO', 'NÚM', 'DEL', 'DE', 'LA', 'EL', 'LOS', 'LAS', 'Y', 'A'])
TARGET_LANG_CODES = {
    'en': 'English', 'bg': 'Bulgarian', 'zh': 'Chinese', 'cs': 'Czech', 'da': 'Danish',
    'nl': 'Dutch', 'et': 'Estonian', 'fi': 'Finnish', 'fr': 'French', 'de': 'German',
    'el': 'Greek', 'hr': 'Croatian', 'hu': 'Hungarian', 'it': 'Italian', 'lv': 'Latvian',
    'lt': 'Lithuanian', 'mt': 'Maltese', 'no': 'Norwegian', 'pl': 'Polish', 'pt': 'Portuguese',
    'ro': 'Romanian', 'ru': 'Russian', 'sk': 'Slovak', 'sr': 'Serbian', 'sl': 'Slovenian',
    'es': 'Spanish', 'sv': 'Swedish', 'tr': 'Turkish', 'us': 'English', 'ar': 'Arabic'
}
MULTI_COLUMN_THRESHOLD_PERCENT = 0.3

def get_language_name(code):
    return TARGET_LANG_CODES.get(code, 'Unknown')

def detect_language_limited_langdetect(text):
    alpha_count = sum(c.isalpha() for c in text)
    if len(text) > 0 and alpha_count / len(text) < MIN_ALPHA_RATIO_FOR_LANG_DETECTION:
        return None
    words = re.findall(r'\b\w+\b', text.upper())
    if any(word in COMMON_SPANISH_WORDS for word in words):
        return 'es'
    try:
        lang_code = detect(text)
        return lang_code if lang_code in TARGET_LANG_CODES else None
    except:
        return None

def get_word_count(phrase):
    words = phrase.split()
    meaningful_words = [word for word in words if word.strip('.')]
    return len(meaningful_words)

def determine_page_layout(page, expected_layout, multi_column_threshold):
    if expected_layout == 'single':
        return 'single'
    elif expected_layout == 'multi':
        return 'multi'
    else:
        left_x_coords = sorted(list(set(b[0] for b in page.get_text("blocks"))))
        if len(left_x_coords) > 1 and left_x_coords[1] > page.rect.width * multi_column_threshold:
            return 'multi'
        else:
            return 'single'

def extract_paragraph_blocks(pdf_path, expected_layout='single', multi_column_threshold=0.3):
    start_time = time.time()
    doc = fitz.open(pdf_path)
    paragraphs = []
    page_layouts = {}

    for page_num, page in enumerate(doc, start=1):
        layout = determine_page_layout(page, expected_layout, multi_column_threshold)
        page_layouts[page_num] = layout
        blocks = page.get_text("blocks")
        if not blocks:
            continue
        current_paragraph = ""
        last_block_bottom = None
        for i, block in enumerate(blocks):
            x0, y0, x1, y1, text, block_no, block_type = block
            if x0 < page.rect.width * TOC_LEFT_THRESHOLD_PERCENT and get_word_count(text) <= MAX_HEADING_WORDS and y1 < page.rect.height * 0.7:
                continue
            if block_type == 0:
                if last_block_bottom is not None and abs(y0 - last_block_bottom) < 5:
                    current_paragraph += " " + text.strip()
                else:
                    if current_paragraph and get_word_count(current_paragraph) >= MIN_PARAGRAPH_WORDS:
                        paragraphs.append({'page': page_num, 'layout': layout, 'text': current_paragraph.strip()})
                    current_paragraph = text.strip()
                last_block_bottom = y1
        if current_paragraph and get_word_count(current_paragraph) >= MIN_PARAGRAPH_WORDS:
            paragraphs.append({'page': page_num, 'layout': layout, 'text': current_paragraph.strip()})
    end_time = time.time()
    extraction_time = end_time - start_time
    st.sidebar.write(f"⏱️ Extraction time: {extraction_time:.2f} seconds")
    return pd.DataFrame(paragraphs)

def analyze_paragraphs_language(df_paragraphs):
    analyzed_data = []
    for index, row in df_paragraphs.iterrows():
        text = row['text']
        lang_code = detect_language_limited_langdetect(text)
        language = get_language_name(lang_code)
        analyzed_data.append({
            'page': row['page'],
            'layout': row['layout'],
            'word_count': get_word_count(text),
            'text': text,
            'language_code': lang_code,
            'language': language
        })
    df_analyzed = pd.DataFrame(analyzed_data)
    major_language = 'Unknown'
    if not df_analyzed.empty:
        language_counts = Counter(df_analyzed['language'])
        if language_counts:
            major_language = language_counts.most_common(1)[0][0]
        df_analyzed['is_foreign'] = df_analyzed['language'] != major_language
        df_analyzed['is_major'] = df_analyzed['language'] == major_language
    else:
        df_analyzed['is_foreign'] = False
        df_analyzed['is_major'] = False
    st.sidebar.write(f"✅ Major language detected: {major_language}")
    return df_analyzed

def verify_foreign_language_google(df_foreign, enable_google_verification=True):
    df_foreign['google_verified_language'] = None
    if not enable_google_verification:
        st.sidebar.warning("Google Translate verification is disabled.")
        return df_foreign
    st.sidebar.info("⏳ Verifying foreign languages using Google Translate...")
    for index, row in df_foreign.iterrows():
        text = row['text']
        try:
            detection = translator.detect(text)
            detected_lang_code = detection.lang
            if detected_lang_code in LANGUAGES:
                df_foreign.loc[index, 'google_verified_language'] = LANGUAGES[detected_lang_code].capitalize()
            else:
                df_foreign.loc[index, 'google_verified_language'] = 'Unknown (Google)'
        except Exception as e:
            st.sidebar.error(f"🚫 Google Translate error for: '{text[:50]}...' - {e}")
            df_foreign.loc[index, 'google_verified_language'] = 'Error (Google)'
            time.sleep(0.1) # Be gentle with the API
    st.sidebar.success("✅ Google Translate verification complete.")
    return df_foreign

def main():
    st.title("Foreign Language Detection in PDFs")

    pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if pdf_file is not None:
        st.sidebar.header("Settings")
        layout_option = st.sidebar.selectbox(
            "Select PDF Layout",
            ["Auto", "Single Column", "Multi Column"]
        )
        expected_layout = 'auto'
        if layout_option == "Single Column":
            expected_layout = 'single'
        elif layout_option == "Multi Column":
            expected_layout = 'multi'

        enable_google_verification = st.sidebar.checkbox("Verify with Google Translate", value=False)

        if st.button("Process PDF"):
            with st.spinner("Extracting text and detecting languages..."):
                df_paragraphs = extract_paragraph_blocks(pdf_file, expected_layout, MULTI_COLUMN_THRESHOLD_PERCENT)

            if not df_paragraphs.empty:
                with st.spinner("Analyzing language..."):
                    df_language_analysis = analyze_paragraphs_language(df_paragraphs)

                major_lang = ""
                major_langs = df_language_analysis.loc[df_language_analysis['is_major'] == True]['language'].unique().astype(str)
                if len(major_langs) > 0:
                    major_lang = ", ".join(major_langs)

                df_foreign = df_language_analysis.loc[
                    (df_language_analysis['is_foreign'] == True) &
                    (df_language_analysis['word_count'] >= 5) &
                    (df_language_analysis['language'] != 'Unknown')
                ].copy()

                if not df_foreign.empty and enable_google_verification:
                    with st.spinner("Verifying with Google Translate..."):
                        df_foreign_verified = verify_foreign_language_google(df_foreign.copy(), enable_google_verification)
                        df_display = df_foreign_verified.loc[df_foreign_verified['google_verified_language'] != major_lang][['page', 'word_count', 'text', 'language', 'google_verified_language']]
                else:
                    df_display = df_foreign[['page', 'word_count', 'text', 'language']]
                    if not df_display.empty and not enable_google_verification:
                        st.sidebar.info("Enable Google Translate in the sidebar for potential verification.")

                if not df_display.empty:
                    st.subheader("Detected Foreign Language Segments")
                    st.write(f"Major Language(s): {major_lang}")
                    st.dataframe(df_display)
                else:
                    st.info(f"No significant foreign language segments detected (excluding '{major_lang}').")

            else:
                st.warning("Could not extract text from the PDF.")

if __name__ == "__main__":
    main()


