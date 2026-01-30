import streamlit as st
import requests
import base64


#Title
st.title("Personal Shopping Assistant")

#Image link and search
with st.form("search_form"):
    url = st.text_input("Paste an image URL:")
    submitted = st.form_submit_button("Search")

if submitted:

    #Display the input image
    st.image(url, caption="Your image", width=300)
    response = requests.get("https://api-520917056692.europe-west1.run.app/predict",
                            params={"image_path": url, "top_k": 5})

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
