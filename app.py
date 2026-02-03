import streamlit as st
import requests
import base64
import random


#Header - fixed for dark mode
st.markdown("""
<style>
header[data-testid="stHeader"] {
    background-color: transparent;
    padding: 10px 20px;
}
header[data-testid="stHeader"]::after {
    content: "Your Personal Shopping Assistant";
    font-size: 14px;
    color: inherit;
    position: absolute;
    left: 20px;
    top: 15px;
}
.price-tag {
    background-color: #FFD700;
    color: black;
    font-weight: bold;
    font-size: 1.4em;
    padding: 5px 15px;
    border-radius: 5px;
    display: inline-block;
    margin: 10px 0;
}
.section-header {
    font-size: 1.1em;
    color: #666;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

#Title
st.title("Personal Shopping Assistant")

#Image link and filters
form_col, image_col = st.columns([1, 1])
with form_col:
    with st.form("search_form"):
        url = st.text_input("Paste an image URL:")
        gender = st.selectbox("Gender (optional)", ["All", "Menswear", "Ladieswear", "Baby/Children"])
        subcategory = st.selectbox("Category (optional):", ['Auto', 'Boots', 'Sneakers', 'Sandals', 'Slippers', 'Flat shoe', 'Heels'])
        button_col, topk_col = st.columns([1, 1])
        with button_col:
            submitted = st.form_submit_button("Search")
        with topk_col:
            top_k = st.selectbox("Number of results", [1, 2, 3, 4, 5], index=4)

#Save results to session state on search
if submitted:
    params = {"image_path": url, "top_k": top_k}
    if gender and gender != "All":
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

    idx = st.slider("Browse recommendations", min_value=1, max_value=len(results), value=1) - 1
    img = results[idx]
    price = prices[idx] if idx < len(prices) else random.randint(30, 100)
    freq_price = freq_prices[idx] if idx < len(freq_prices) else random.randint(30, 100)

    # Similar item section
    st.markdown('<p class="section-header"> Similar Product:</p>', unsafe_allow_html=True)
    img_col, info_col = st.columns([1, 1])
    with img_col:
        st.image(base64.b64decode(img["data"]), width=300)
    with info_col:
        st.markdown(f"**{img.get('name', '')}**")
        st.markdown(f'<span class="price-tag">€{price}</span>', unsafe_allow_html=True)
        st.text(f"Category: {img.get('subcategory', 'Unknown')}")
        st.text(f"Gender: {img.get('gender', 'Unknown')}")

    # Frequently bought together section (mock data - using same image as placeholder)
    st.markdown("---")
    st.markdown('<p class="section-header"> Frequently Bought Together:</p>', unsafe_allow_html=True)
    freq_col, freq_info_col = st.columns([1, 1])
    with freq_col:
        # Using same image as mock - in production this would be different data from API
        st.image(base64.b64decode(img["data"]), width=300)
    with freq_info_col:
        st.markdown(f"**Matching {img.get('subcategory', 'Item')}**")
        st.markdown(f'<span class="price-tag">€{freq_price}</span>', unsafe_allow_html=True)
        st.text(f"Category: {img.get('subcategory', 'Unknown')}")
        st.text(f"Gender: {img.get('gender', 'Unknown')}")
