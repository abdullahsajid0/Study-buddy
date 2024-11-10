import os
import streamlit as st
from groq import Groq
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

# Initialize Streamlit session state for calculator input
if "calculator_input" not in st.session_state:
    st.session_state["calculator_input"] = ""
if "calculator_result" not in st.session_state:
    st.session_state["calculator_result"] = ""
if "memory_value" not in st.session_state:
    st.session_state["memory_value"] = None

# Access the secret API key
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    st.error("API key not found. Please set the GROQ_API_KEY environment variable.")
client = Groq(api_key=api_key)

# Define a helper function to interact with Groq API
def ask_groq(prompt):
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# Define the calculator display and button functionalities
def display_calculator():
    st.write("### Scientific Calculator")
    st.text_input("Expression", value=st.session_state["calculator_input"], disabled=True, key="expression_display")
    for row in calculator_buttons:
        cols = st.columns(len(row))
        for i, button in enumerate(row):
            if cols[i].button(button):
                handle_calculator_button(button)
    if st.session_state["calculator_result"]:
        st.write("### Result:")
        st.write(st.session_state["calculator_result"])

# Button handling logic
def handle_calculator_button(button):
    if button == "Clear":
        st.session_state["calculator_input"] = ""
        st.session_state["calculator_result"] = ""
    elif button == "=":
        solve_expression_with_model()
    elif button == "graph":
        plot_graph()
    elif button == "solve":
        solve_expression_with_model()
    elif button == "M+":
        st.session_state["memory_value"] = st.session_state["calculator_input"]
    elif button == "M-":
        st.session_state["memory_value"] = None
    elif button == "MR":
        if st.session_state["memory_value"]:
            st.session_state["calculator_input"] += st.session_state["memory_value"]
    else:
        st.session_state["calculator_input"] += button

# Use Groq model to solve the math problem
def solve_expression_with_model():
    prompt = f"Solve this mathematical expression: {st.session_state['calculator_input']}"
    result = ask_groq(prompt)
    st.session_state["calculator_result"] = result if result else "Error solving expression."

# Function to plot the graph if "x" is present in expression
def plot_graph():
    if "x" in st.session_state["calculator_input"]:
        try:
            x = sp.symbols("x")
            expr = sp.sympify(st.session_state["calculator_input"])
            func = sp.lambdify(x, expr, "numpy")
            x_vals = np.linspace(-10, 10, 400)
            y_vals = func(x_vals)

            plt.figure(figsize=(8, 4))
            plt.plot(x_vals, y_vals, label=str(expr))
            plt.xlabel("x")
            plt.ylabel("f(x)")
            plt.title("Graph of the Function")
            plt.legend()
            plt.grid(True)
            st.pyplot(plt)
        except Exception as e:
            st.error("Could not plot graph. Please enter a valid expression.")
    else:
        st.error("Graphing requires 'x' in the expression.")

# Define main app with calculator display
def main():
    st.title("Study Buddy AI App")
    st.write("Powered by Groq AI and Streamlit")

    st.sidebar.title("Choose a Feature")
    feature = st.sidebar.radio(
        "Go to",
        ["Concept Explanation", "Personalized Study Plan", "Scientific Calculator", "Study Tips & Time Management"]
    )

    if feature == "Concept Explanation":
        st.header("Explain a Concept")
        concept = st.text_input("Enter a concept you'd like explained")
        if st.button("Explain") and concept:
            prompt = f"Explain the concept of {concept} in simple terms."
            explanation = ask_groq(prompt)
            st.write("*Explanation:*", explanation if explanation else "Error fetching explanation.")

    elif feature == "Personalized Study Plan":
        st.header("Generate a Study Plan")
        subject = st.text_input("Enter the subject")
        topic = st.text_input("Enter the topic")
        duration = st.number_input("Enter study duration in hours", min_value=1)
        purpose = st.selectbox("Purpose", ["Exam Preparation", "Test Preparation"])
        
        if st.button("Generate Plan") and subject and topic and duration:
            prompt = f"Create a study plan for {duration} hours on {topic} in {subject} for {purpose.lower()}."
            study_plan = ask_groq(prompt)
            st.write("*Study Plan:*", study_plan if study_plan else "Error generating study plan.")

    elif feature == "Scientific Calculator":
        display_calculator()

    elif feature == "Study Tips & Time Management":
        st.header("Get a Study Tip")
        if st.button("Get Tip"):
            prompt = "Provide one study tip for students."
            tip = ask_groq(prompt)
            st.write("*Study Tip:*", tip if tip else "Error fetching tip.")

if __name__ == "__main__":
    main()



