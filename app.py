import os
import streamlit as st
from groq import Groq
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

# ===============================
# Setup Groq API Client
# ===============================
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    st.error("API key not found. Please set the GROQ_API_KEY environment variable.")
else:
    client = Groq(api_key=api_key)

# ===============================
# Helper: Ask Groq
# ===============================
def ask_groq(prompt):
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="openai/gpt-oss-120b",
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# ===============================
# Graph Plotter (local sympy)
# ===============================
def plot_graph(expression):
    if "x" not in expression:
        st.warning("To plot, your expression must include 'x'.")
        return

    try:
        x = sp.symbols("x")
        expr = sp.sympify(expression)
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
        st.error(f"Error plotting graph: {e}")

# ===============================
# Desmos Embedded Calculator
# ===============================
def desmos_calculator():
    st.subheader("🧮 Free Desmos Calculator")

    calc_type = st.radio(
        "Choose calculator type:",
        ["Scientific Calculator", "Graphing Calculator"],
        horizontal=True
    )

    if calc_type == "Scientific Calculator":
        st.components.v1.iframe("https://www.desmos.com/scientific", height=600)
    else:
        st.components.v1.iframe("https://www.desmos.com/calculator", height=600)

    st.info("Desmos calculators are completely free for educational and personal use.")

# ===============================
# Main App
# ===============================
def main():
    st.title("📚 Study Buddy AI App")
    st.write("Powered by **Groq AI** and **Streamlit**")

    st.sidebar.title("🧭 Navigation")
    feature = st.sidebar.radio(
        "Choose a Feature",
        [
            "Concept Explanation",
            "Personalized Study Plan",
            "AI Scientific Assistant",
            "Desmos Calculator",
            "Study Tips & Time Management"
        ]
    )

    # -------------------------------
    # Concept Explanation
    # -------------------------------
    if feature == "Concept Explanation":
        st.header("🧠 Explain a Concept")
        concept = st.text_input("Enter a concept you'd like explained")

        if st.button("Explain") and concept:
            prompt = f"Explain the concept of {concept} in simple, student-friendly terms."
            explanation = ask_groq(prompt)
            if explanation:
                st.success(explanation)
            else:
                st.error("Error fetching explanation.")

    # -------------------------------
    # Personalized Study Plan
    # -------------------------------
    elif feature == "Personalized Study Plan":
        st.header("📅 Generate a Study Plan")

        subject = st.text_input("Enter the subject")
        topic = st.text_input("Enter the topic")
        duration = st.number_input("Enter study duration (in hours)", min_value=1)
        purpose = st.selectbox("Purpose", ["Exam Preparation", "Test Preparation"])

        if st.button("Generate Plan") and subject and topic:
            prompt = f"Create a {duration}-hour study plan for {topic} in {subject} for {purpose.lower()}."
            plan = ask_groq(prompt)
            if plan:
                st.success(plan)
            else:
                st.error("Error generating study plan.")

    # -------------------------------
    # AI Scientific Assistant (local math + AI fallback)
    # -------------------------------
    elif feature == "AI Scientific Assistant":
        st.header("🔢 AI Scientific Assistant")

        expression = st.text_input("Enter a math expression (you can use x for graphing):")

        col1, col2, col3 = st.columns(3)
        if col1.button("Calculate"):
            try:
                result = sp.sympify(expression).evalf()
                st.success(f"Result: {result}")
            except Exception:
                st.warning("Could not compute locally, asking AI...")
                ai_result = ask_groq(f"Solve this mathematical expression: {expression}")
                if ai_result:
                    st.info(ai_result)
                else:
                    st.error("Unable to solve expression.")
        if col2.button("Graph"):
            plot_graph(expression)
        if col3.button("Clear"):
            st.experimental_rerun()

    # -------------------------------
    # Desmos Embedded Calculator
    # -------------------------------
    elif feature == "Desmos Calculator":
        desmos_calculator()

    # -------------------------------
    # Study Tips
    # -------------------------------
    elif feature == "Study Tips & Time Management":
        st.header("💡 Study Tips & Time Management")
        if st.button("Get a Tip"):
            tip = ask_groq("Provide one effective study tip for students.")
            if tip:
                st.success(tip)
            else:
                st.error("Error fetching study tip.")

# ===============================
# Run the App
# ===============================
if __name__ == "__main__":
    main()
