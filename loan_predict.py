import streamlit as st
import pickle
# Define the function for the first page (Form)
def page_form():
    st.markdown("<span style='color: #AAAAAA; font-size: 50px; font-weight: 700'>Enter your details</span>",unsafe_allow_html=True)
    credit_history = st.selectbox("Credit History", ["Good", "Bad"])
    applicant_income = st.number_input("Applicant Income", min_value=0)
    coapplicant_income = st.number_input("Coapplicant Income", min_value=0)
    resident_area = st.selectbox("Resident Area", ["Urban", "Semiurban", "Rural"])
    dependents = st.number_input("Dependents", min_value=0, max_value=20)
    education = st.selectbox("Education", ["Graduate", "Not Graduate"])
    married = st.selectbox("Married", ["Yes", "No"])
    loan_term = st.number_input("Loan Term", min_value=0)

    # Submit button
    if st.button("Submit"):
        placeholder.empty()
        st.experimental_set_query_params(
            credit_history=credit_history,
            coapplicant_income=coapplicant_income,
            resident_area=resident_area,
            dependents=dependents,
            education=education,
            married=married,
            loan_term=loan_term
        )
        page_data_display()

def predict(credit_history, coapplicant_income, resident_area, dependents, education, married, loan_term):
    #attribute order for scaler
    #Married	Dependents	Education	Self_Employed	ApplicantIncome	CoapplicantIncome	LoanAmount	Loan_Amount_Term	Credit_History	Property_Area	Loan_Status	Gender_Female	Gender_Male
    lrmodel = pickle.load(open('lrModel.sav', 'rb'))
    scaler = pickle.load(open('scaler.sav', 'rb'))
    input = [[int(married), int(dependents), int(education), 0, 0, float(coapplicant_income), 0, float(loan_term), float(credit_history), int(resident_area), 0, 0, 0]]
    input_scaled = scaler.transform(input)
    prediction = lrmodel.predict([[input_scaled[0][0], input_scaled[0][1],input_scaled[0][2], input_scaled[0][5], input_scaled[0][7], input_scaled[0][8], input_scaled[0][9]]])
    return prediction

def page_data_display():
    if (st.experimental_get_query_params().get("credit_history", "")[0] == "Good"):
        credit_history = 1
    else:
        credit_history = 0
    
    coapplicant_income = float(st.experimental_get_query_params().get("coapplicant_income", "")[0])
    if (st.experimental_get_query_params().get("resident_area", "")[0] == "Urban"):
        resident_area = 2
    elif (st.experimental_get_query_params().get("resident_area", "")[0] == "Semiurban "):
        resident_area = 1
    else:
        resident_area = 0
    

    dependents = int(st.experimental_get_query_params().get("dependents", "")[0])

    if (st.experimental_get_query_params().get("education", "")[0] == "Graduate"):
        education = 0
    else:
        education = 1

    if (st.experimental_get_query_params().get("married", "")[0] == "Yes"):
        married = 1
    else:
        married = 0

    loan_term = float(st.experimental_get_query_params().get("loan_term", "")[0])

    # Display the data from the form
    # st.subheader("Form Data:")
    # st.write(f"Credit History: {credit_history}")
    # st.write(f"Coapplicant Income: {coapplicant_income}")
    # st.write(f"Resident Area: {resident_area}")
    # st.write(f"Dependents: {dependents}")
    # st.write(f"Education: {education}")
    # st.write(f"Married: {married}")
    if (predict(credit_history, coapplicant_income, resident_area, dependents, education, married, loan_term)):
        st.markdown("<span style='color: #039487; font-size: 30px; font-weight: 700'>Your application is highly likely to be approved</span>",unsafe_allow_html=True)
    else:
        st.markdown("<span style='color: #ff9487; font-size: 30px; font-weight: 700'>Your application is highly likely to be rejected</span>",unsafe_allow_html=True)
    st.write("model approval prediction accuracy: 95%")
    # st.markdown(
    #     """
    #         <script>
    #             window.scrollTo(0, document.body.scrollHeight);
    #         </script>
    #     """
    # )
    #st.write(f"LoanStatus: {predict(credit_history, coapplicant_income, resident_area, dependents, education, married, loan_term)}")

# Streamlit app entry point
placeholder = st.empty()
def main():
    page_form()
    #Create a Streamlit sidebar for navigation
    # page = st.sidebar.selectbox("Select a Page", ["Form", "Data Display"])

    # if page == "Form":
    #     page_form()
    # elif page == "Data Display":
    #     page_data_display()

if __name__ == "__main__":
    main()