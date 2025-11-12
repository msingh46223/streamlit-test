import streamlit as st

st.title("Sample User Interface")
st.write(
    "Click the button to import your file."
)

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
if uploaded_file:
    st.write("File uploaded!")
    st.write("**Select Raymond-Roy classification:**")
    stage = st.radio("Raymond-Roy class:",[1,2,3])
#    st.radio("Pick one", ["cats", "dogs"])

    match stage:
        case 1:
            st.write("Recurrence probability is low")
        case 2:
            st.write("Recurrence probability is moderate")
        case 3:
            st.write("Recurrence probability is high")
