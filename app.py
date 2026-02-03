import streamlit as st
import requests
import base64
import random
from pathlib import Path


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
        gender = st.selectbox("Gender (optional)", ["Auto", "Menswear", "Ladieswear", "Baby/Children"])
        subcategory = st.selectbox("Category (optional):", ['Auto', 'Boots', 'Sneakers', 'Sandals', 'Slippers', 'Flat shoe', 'Heels'])
        button_col, topk_col = st.columns([1, 1])
        with button_col:
            submitted = st.form_submit_button("Search")
        with topk_col:
            top_k = st.selectbox("Number of results", [2, 4, 6], index=2)

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
        # Generate random prices for similar items (30-100€)
        st.session_state["prices"] = [random.randint(30, 100) for _ in range(top_k)]
        # Generate random prices for frequently bought items (30-100€)
        st.session_state["freq_prices"] = [random.randint(30, 100) for _ in range(top_k)]
    else:
        st.error(f"API error: {response.status_code} - {response.text}")

#Display input image on the right
if "search_url" in st.session_state:
    with image_col:
        st.image(st.session_state["search_url"], caption="Your image")

#Display results from session state
if "results" in st.session_state:
    st.markdown("### Recommendations:")
    results = st.session_state["results"]
    prices = st.session_state.get("prices", [50] * len(results))
    freq_prices = st.session_state.get("freq_prices", [50] * len(results))

    # Results come in pairs: similar product + frequently bought together
    num_pairs = len(results) // 2
    pair_idx = st.slider("Browse recommendations", min_value=1, max_value=max(1, num_pairs), value=1) - 1

    # Get the pair: similar product (even index) and frequently bought (odd index)
    similar_idx = pair_idx * 2
    freq_idx = pair_idx * 2 + 1

    similar_img = results[similar_idx] if similar_idx < len(results) else None
    freq_img = results[freq_idx] if freq_idx < len(results) else None

    price = prices[similar_idx] if similar_idx < len(prices) else random.randint(30, 100)
    freq_price = freq_prices[freq_idx] if freq_idx < len(freq_prices) else random.randint(30, 100)

    # Similar item section
    if similar_img:
        st.markdown('<p class="section-header"> Similar Product:</p>', unsafe_allow_html=True)
        img_col, info_col = st.columns([1, 1])
        with img_col:
            st.image(base64.b64decode(similar_img["data"]), width=300)
        with info_col:
            st.markdown(f"**{similar_img.get('name', '')}**")
            st.markdown(f'<span class="price-tag">€{price}</span>', unsafe_allow_html=True)
            st.text(f"Category: {similar_img.get('subcategory', 'Unknown')}")
            st.text(f"Gender: {similar_img.get('gender', 'Unknown')}")

    # Frequently bought together section
    if freq_img:
        st.markdown("---")
        st.markdown('<p class="section-header"> Frequently Bought Together:</p>', unsafe_allow_html=True)
        freq_col, freq_info_col = st.columns([1, 1])
        with freq_col:
            st.image(base64.b64decode(freq_img["data"]), width=300)
        with freq_info_col:
            st.markdown(f"**{freq_img.get('name', '')}**")
            st.markdown(f'<span class="price-tag">€{freq_price}</span>', unsafe_allow_html=True)
            st.text(f"Category: {freq_img.get('subcategory', 'Unknown')}")
            st.text(f"Gender: {freq_img.get('gender', 'Unknown')}")
