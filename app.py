import os
import streamlit as st
from groq import Groq
import numpy as np
import matplotlib.pyplot as plt

# Initialize Streamlit session state for calculator input
if "calculator_input" not in st.session_state:
    st.session_state["calculator_input"] = ""

# Initialize session state for the result
if "calculator_result" not in st.session_state:
    st.session_state["calculator_result"] = ""

# Access the secret API key
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

# Define the scientific calculator buttons and functions
calculator_buttons = [
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["0", ".", "^", "+"],
    ["(", ")", "sin", "cos"],
    ["tan", "arcsin", "arccos", "arctan"],
    ["exp", "ln", "log", "sqrt"],
    ["M+", "M-", "MR", "MC"],
    ["Clear", "=", "graph", "solve"]
]

# Memory storage for calculator
memory_value = None

# Apply custom CSS for buttons
st.markdown(
    """
    <style>
    .stButton>button {
        width: 100%;
        padding: 8px;
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        border: none;
        font-size: 16px;
        margin: 2px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Define the calculator display and button functionalities
def display_calculator():
    st.write("### Scientific Calculator")
    
    # Display the current input expression above the calculator
    st.text_input("Expression", value=st.session_state["calculator_input"], disabled=True, key="expression_display")
    
    # Create button grid layout
    for row in calculator_buttons:
        cols = st.columns(len(row))
        for i, button in enumerate(row):
            if cols[i].button(button):
                handle_calculator_button(button)
    
    # Display the result below the buttons
    if st.session_state["calculator_result"]:
        st.write("### Result:")
        st.write(st.session_state["calculator_result"])

# Button handling logic
def handle_calculator_button(button):
    global memory_value
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
        memory_value = st.session_state["calculator_input"]
    elif button == "M-":
        memory_value = None
    elif button == "MR":
        if memory_value is not None:
            st.session_state["calculator_input"] += memory_value
    elif button == "MC":
        st.session_state["calculator_input"] = ""
        memory_value = None
    else:
        # Append button press to calculator input
        st.session_state["calculator_input"] += button

# Use Groq model to solve the math problem
def solve_expression_with_model():
    try:
        prompt = f"Solve this mathematical expression: {st.session_state['calculator_input']}"
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
        )
        result = response.choices[0].message.content
        st.session_state["calculator_result"] = result
    except Exception as e:
        st.error(f"Error in solving math problem: {e}")

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
    st.title("Student-Assisting AI App")
    st.write("Powered by Groq AI and Streamlit")

    # Sidebar for navigation
    st.sidebar.title("Choose a Feature")
    feature = st.sidebar.radio(
        "Go to",
        [
            "Concept Explanation",
            "Personalized Study Plan",
            "Scientific Calculator",
            "Study Tips & Time Management",
        ],
    )

    # Concept Explanation Feature
    if feature == "Concept Explanation":
        st.header("Explain a Concept")
        concept = st.text_input("Enter a concept you'd like explained")
        
        if st.button("Explain"):
            if concept:
                prompt = f"Explain the concept of {concept} in simple terms."
                response = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama3-8b-8192",
                )
                explanation = response.choices[0].message.content
                st.write("*Explanation:*", explanation)
            else:
                st.write("Please enter a concept to get an explanation.")

    # Personalized Study Plan Feature
    elif feature == "Personalized Study Plan":
        st.header("Generate a Study Plan")
        subject = st.text_input("Enter the subject")
        topic = st.text_input("Enter the topic")
        duration = st.number_input("Enter study duration in hours", min_value=1)
        purpose = st.selectbox("Purpose", ["Exam Preparation", "Test Preparation"])
        
        if st.button("Generate Plan"):
            if subject and topic and duration:
                prompt = f"Create a study plan for {duration} hours on {topic} in {subject} for {purpose.lower()}."
                response = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama3-8b-8192",
                )
                study_plan = response.choices[0].message.content
                st.write("*Study Plan:*")
                st.write(study_plan)
            else:
                st.write("Please enter all required details to generate a study plan.")

    # Scientific Calculator Feature
    elif feature == "Scientific Calculator":
        display_calculator()

    # Study Tips & Time Management Feature
    elif feature == "Study Tips & Time Management":
        st.header("Get a Study Tip")

        if st.button("Get Tip"):
            prompt = "Provide one study tip for students."
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama3-8b-8192",
            )
            tip = response.choices[0].message.content
            st.write("*Study Tip:*")
            st.write(tip)

if __name__ == "__main__":
    main()
