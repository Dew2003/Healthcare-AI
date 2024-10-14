st.markdown("<h2>Disease Detection</h2>", unsafe_allow_html=True)
    
    symptoms_input = st.text_input("Enter symptoms separated by commas (e.g., itching, skin rash, fatigue):")

    if st.button("🔍 Predict Disease"):
        if symptoms_input:
            with st.spinner('Analyzing Symptoms...'):
                user_symptoms = [s.strip() for s in symptoms_input.split(',')]
                try:
                    predicted_disease = disease_backend.get_predicted_value(user_symptoms)
                    dis_des, precautions, medications, rec_diet, workout = disease_backend.helper(predicted_disease)

                    st.markdown(f"<h3>Predicted Disease: {predicted_disease}</h3>", unsafe_allow_html=True)
                    st.write(f"**Description**: {dis_des}")

                    st.write("### Precautions")
                    st.write("\n".join([f"- {pre}" for pre in precautions[0]]))

                    st.write("### Medications")
                    st.write("\n".join([f"- {med}" for med in medications]))

                    st.write("### Recommended Diet")
                    st.write("\n".join([f"- {diet}" for diet in rec_diet]))

                    st.write("### Suggested Workout")
                    st.write(workout)
                except KeyError:
                    st.error("Some symptoms might be misspelled or not recognized. Please try again.")
        else:
            st.error("Please enter symptoms to predict the disease.")
--------------------------------------------------------------------------------------




