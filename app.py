import streamlit as st
import requests
import base64


#Header
st.markdown("""
<style>
header[data-testid="stHeader"] {
    background-color: white;
    padding: 10px 20px;
}
header[data-testid="stHeader"]::after {
    content: "Your Personal Shopping Assistant";
    font-size: 14px;
    color: gray;
    position: absolute;
    left: 20px;
    top: 15px;
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
        subcategory = st.selectbox("Category (optional):", ['Boots', 'Sneakers', 'Other shoe', 'Sandals', 'Slippers', 'Ballerinas', 'Flat shoe', 'Wedge', 'Pumps', 'Flip flop', 'Bootie', 'Heeled sandals', 'Flat shoes', 'Heels', 'Moccasins', 'Pre-walkers'])
        button_col, topk_col = st.columns([1, 1])
        with button_col:
            submitted = st.form_submit_button("Search")
        with topk_col:
            top_k = st.selectbox("Number of results", [1, 2, 3, 4, 5], index=4)

#Save results to session state on search
if submitted:
    params = {"image_path": url, "top_k": top_k}
    if gender != "All":
        params["gender"] = gender
    if subcategory:
        params["subcategory"] = subcategory

    response = requests.get("https://api-520917056692.europe-west1.run.app/predict",
                            params=params)

    if response.status_code == 200:
        st.session_state["results"] = response.json()
        st.session_state["search_url"] = url
    else:
        st.error("API error")

#Display input image on the right
if "search_url" in st.session_state:
    with image_col:
        st.image(st.session_state["search_url"], caption="Your image")

#Display results from session state
if "results" in st.session_state:
    st.markdown("### Recommendations:")
    results = st.session_state["results"]
    idx = st.slider("Browse recommendations", min_value=1, max_value=len(results), value=1) - 1
    img = results[idx]
    img_col, info_col = st.columns([1, 1])
    with img_col:
        st.image(base64.b64decode(img["data"]), width=300)
    with info_col:
        st.markdown(f"**{img.get('name', '')}**")
        st.text(f"Category: {img.get('subcategory', 'Unknown')}")
        st.text(f"Gender: {img.get('gender', 'Unknown')}")
