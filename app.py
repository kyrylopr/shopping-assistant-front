import streamlit as st
import requests
import base64
from pathlib import Path

# Set page config with favicon (must be first Streamlit command)
st.set_page_config(
    page_title="Shopping Assistant",
    page_icon="assets/favicon.svg"
)

# Load CSS from external file
def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css(Path(__file__).parent / "styles.css")

#Title
#st.title("Personal Shopping Assistant")

#Image link and filters
form_col, image_col = st.columns([1, 1])
with form_col:
    with st.form("search_form"):
        url = st.text_input("Paste an image URL:")
        gender = st.selectbox("Group (optional):", ["Auto", "Menswear", "Ladieswear", "Baby/Children"])
        subcategory = st.selectbox("Category (optional):", ['Auto', 'Boots', 'Sneakers', 'Sandals', 'Slippers', 'Flat shoe', 'Heels'])
        button_col, topk_col = st.columns([1, 1])
        with button_col:
            submitted = st.form_submit_button("Search")
        with topk_col:
            top_k = st.selectbox("Number of results", [2, 4, 6, 8], index=2)

#Save results to session state on search
if submitted:
    params = {"image_path": url, "top_k": top_k}
    if gender and gender != "Auto":
        params["gender"] = gender
    # Only add subcategory if it's not Auto (Auto means let the model decide)
    if subcategory and subcategory not in ["Auto", "None", ""]:
        params["subcategory"] = subcategory

    response = requests.get("https://api-520917056692.europe-west1.run.app/predict",
                            params=params)

    if response.status_code == 200:
        st.session_state["results"] = response.json()
        st.session_state["search_url"] = url
    else:
        st.error(f"API error: {response.status_code} - {response.text}")

#Display input image on the right
if "search_url" in st.session_state:
    with image_col:
        st.image(st.session_state["search_url"], caption="Provided Example")

#Display results from session state
if "results" in st.session_state:
    st.markdown("### Recommendations:")
    results = st.session_state["results"]

    # Results: first half = similar items, second half = sales suggestions
    num_pairs = len(results) // 2
    if num_pairs > 1:
        pair_idx = st.slider("", min_value=1, max_value=num_pairs, value=1, label_visibility="collapsed") - 1
    else:
        pair_idx = 0

    # Get the pair: similar product (first half) + frequently bought (second half)
    similar_idx = pair_idx
    freq_idx = pair_idx + num_pairs

    similar_img = results[similar_idx] if similar_idx < len(results) else None
    freq_img = results[freq_idx] if freq_idx < len(results) else None

    # Similar item section
    if similar_img:
        img_col, info_col = st.columns([1, 1])
        with img_col:
            st.image(base64.b64decode(similar_img["data"]), width=300)
        with info_col:
            st.markdown('<p class="section-header">Similar Product:</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="product-name">{similar_img.get("name", "")}</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="product-price">Price: €{similar_img.get("price", 0)}</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="product-info">Category: {similar_img.get("subcategory", "Unknown").replace("Subcategory: ", "")}</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="product-info">{similar_img.get("gender", "Unknown").replace("Gender: ", "")}</p>', unsafe_allow_html=True)

    # Frequently bought together section
    if freq_img:
        st.markdown("---")
        freq_col, freq_info_col = st.columns([1, 1])
        with freq_col:
            st.image(base64.b64decode(freq_img["data"]), width=300)
        with freq_info_col:
            st.markdown('<p class="section-header">Frequently Bought Together:</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="product-name">{freq_img.get("name", "")}</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="product-price">Price: €{freq_img.get("price", 0)}</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="product-info">Category: {freq_img.get("subcategory", "Unknown").replace("Subcategory: ", "")}</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="product-info">{freq_img.get("gender", "Unknown").replace("Gender: ", "")}</p>', unsafe_allow_html=True)
