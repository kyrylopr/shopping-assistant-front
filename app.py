import streamlit as st
import requests
import base64


#Title
st.title("Personal Shopping Assistant")

#Image link and filters
with st.form("search_form"):
    url = st.text_input("Paste an image URL:")
    gender = st.selectbox("Gender (optional)", ["All", "Menswear", "Ladieswear", "Baby/Children"])
    subcategory = st.selectbox("Subcategory (optional):", ['Boots', 'Sneakers', 'Other shoe', 'Sandals', 'Slippers', 'Ballerinas', 'Flat shoe', 'Wedge', 'Pumps', 'Flip flop', 'Bootie', 'Heeled sandals', 'Flat shoes', 'Heels', 'Moccasins', 'Pre-walkers'])
    button_col, slider_col = st.columns([1, 3])
    with button_col:
        submitted = st.form_submit_button("Search")
    with slider_col:
        top_k = st.slider("Number of results", min_value=1, max_value=5, value=5)

if submitted:

    #Display the input image
    st.image(url, caption="Your image", width=300)

    #Build API params
    params = {"image_path": url, "top_k": top_k}
    if gender != "All":
        params["gender"] = gender
    if subcategory:
        params["subcategory"] = subcategory

    #Call the API
    response = requests.get("https://api-520917056692.europe-west1.run.app/predict",
                            params=params)

    if response.status_code == 200:
        st.markdown("### Recommendations:")
        results = response.json()
        cols = st.columns(len(results))
        for col, img in zip(cols, results):
            col.image(base64.b64decode(img["data"]), caption=img["name"])
            col.markdown(f"**{img.get('description', '')}**")
            col.text(f"Category: {img.get('subcategory', 'Unknown')}")
            col.text(f"Gender: {img.get('gender', 'Unknown')}")
    else:
        st.error("API error")
