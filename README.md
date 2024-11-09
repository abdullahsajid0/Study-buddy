

# Study Buddy AI App

### Powered by Groq AI and Streamlit

The **Study Budy AI App** is an interactive application built with Streamlit and powered by Groq AI, designed to enhance students' learning experiences. This app includes features for concept explanation, personalized study plans, a scientific calculator, and study tips, all in one place.

## Features

1. **Concept Explanation**
   - Students can enter any concept or topic they need help with. The app uses AI to generate a clear, simple explanation to aid understanding.

2. **Personalized Study Plan**
   - Students can create a tailored study plan by specifying the subject, topic, and study duration. This helps organize study time effectively for different academic purposes.

3. **Scientific Calculator**
   - A fully-featured scientific calculator with common mathematical functions and memory operations. It supports basic arithmetic, trigonometry, logarithmic functions, and graph plotting for expressions with variables.

4. **Study Tips & Time Management**
   - Provides study tips and time management advice, including techniques like the Pomodoro Technique to help students study more effectively.

## Technical Specifications

- **Groq AI**: The app leverages Groq AI for generating explanations, study plans, and tips through natural language processing.
- **Streamlit**: The app interface is built with Streamlit, allowing for a user-friendly and interactive web experience.
- **Additional Libraries**: Uses `numpy` and `matplotlib` for calculations and graph plotting in the scientific calculator feature.

## Setup and Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/student-assisting-ai-app.git
   cd student-assisting-ai-app
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up the API Key**:
   - Add your Groq API key to your environment by creating a `.env` file or exporting it directly:
   ```bash
   export GROQ_API_KEY="your_api_key"
   ```

4. **Run the app**:
   ```bash
   streamlit run app.py
   ```

## Usage Guide

1. **Concept Explanation**:
   - Navigate to the "Concept Explanation" feature in the sidebar, input a concept, and click "Explain" to get an AI-driven explanation.

2. **Personalized Study Plan**:
   - Go to "Personalized Study Plan" in the sidebar. Enter the subject, topic, and duration, and select the purpose. Click "Generate Plan" to receive a structured study plan.

3. **Scientific Calculator**:
   - Select "Scientific Calculator" from the sidebar. Use the interactive calculator interface to input expressions and click "=" to solve. You can also plot graphs by including variables like 'x'.

4. **Study Tips & Time Management**:
   - In the sidebar, click on "Study Tips & Time Management." Press "Get Tip" to receive a study tip that helps improve focus and productivity.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests to add features, fix bugs, or improve the app’s functionality.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

