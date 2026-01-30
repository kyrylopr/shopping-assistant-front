import streamlit as st
import requests
import base64

# ----------------------
# Base API URL
# ----------------------
API_URL = "https://api-520917056692.europe-west1.run.app/predict"

# ----------------------
# Page config with shopping cart sticker favicon
# ----------------------
st.set_page_config(
    page_title="Personal Shopping Assistant",
    page_icon="https://em-content.zobj.net/thumbs/240/apple/325/shopping-cart_1f6d2.png",
    layout="wide"
)

# ----------------------
# Load external CSS
# ----------------------
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ----------------------
# Header
# ----------------------
st.markdown("<h1 style='text-align:center;'>Personal Shopping Assistant</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center; color:#666;'>Select a category, gender, and paste a product link. We provide 5 suggestions.</p>",
    unsafe_allow_html=True
)
st.write("")

# ----------------------
# User input dropdowns
# ----------------------
col1, col2, col3 = st.columns(3)

with col1:
    category = st.selectbox("Category", ["Shoes", "Shirts", "Pants", "Accessories", "Other"])

with col2:
    gender = st.selectbox("Gender", ["Men", "Women", "Unisex", "Kids"])

with col3:
    brand = st.selectbox("Brand", ["Any", "Nike", "Adidas", "Puma", "Other"])

st.write("")
image_url = st.text_input("Product link", placeholder="Paste a product URL here")
st.write("")

# ----------------------
# Action button
# ----------------------
if st.button("Get Suggestions"):
    if not image_url:
        st.warning("Please paste a product link.")
    else:
        st.success("Here are some suggested products:")

        # ----------------------
        # Call deployed API
        # ----------------------
        try:
            params = {
                "image_path": image_url,
                "top_k": 5,
                "category": category,
                "gender": gender,
                "brand": brand
            }
            response = requests.get(API_URL, params=params)
            suggestions = response.json()  # List of suggestions

            # ----------------------
            # Combine input + suggestions into horizontal row
            # ----------------------
            cards_html = "<div class='product-grid'>"

            # Input card
            cards_html += f"""
            <div class='product-card'>
                <img src='{image_url}' />
                <h4>Your input</h4>
            </div>
            """

            # Suggested products
            for product in suggestions:
                cards_html += f"""
                <div class='product-card'>
                    <img src='data:image/jpeg;base64,{product["data"]}' />
                    <h4>{product["name"]}</h4>
                </div>
                """

            cards_html += "</div>"
            st.markdown(cards_html, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Could not fetch suggestions from the model: {e}")

# ----------------------
# Footer
# ----------------------
st.markdown("<div class='footer'>Minimal. Neutral. Modern.</div>", unsafe_allow_html=True)
