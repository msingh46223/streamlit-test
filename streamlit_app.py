import streamlit as st

st.title("Sample User Interface")
st.write(
    "Click the button to import your file."
)

uploaded_file = st.file_uploader("Upload the aneurysm file")
if uploaded_file:
    st.write("File uploaded!")
    prob = 5 #init probability



    #st.write("Select Raymond-Roy classification:")
    stage = st.radio("**Raymond-Roy class:**",[1,2,3])
#    st.radio("Pick one", ["cats", "dogs"])

    match stage:
        case 1:
            prob += 2
        case 2:
            prob += 24
        case 3:
            prob += 39
    
    age = st.number_input("**Patient Age:**", 0, 125)
    if age > 25:
        prob += ((age-25)//2)

    sex = st.radio("**Patient Sex:**", ["Female","Male","Unknown"])
    match sex:
        case "Female":
            prob -= 5
        case "Male":
            prob += 5

    smoker = st.radio("**Patient Smoking Status:**", ["Nonsmoker","Smoker","Quit smoking within last 6 months"])
    match smoker:
        case "Nonsmoker":
            prob -= int(prob * .48)
        case "Smoker":
            prob = prob
        case "Quit smoking within last 6 months":
            prob -= int(prob * .23)
    
    probstr = str(prob)
    st.write("Recurrence probability is " + probstr + "%")
