import streamlit as st
import groq
import os
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="AutoDoc AI",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Groq client
GROQ_API_KEY = "#Replace with your groq api key"
client = groq.Groq(api_key=GROQ_API_KEY)

# Custom CSS for professional styling and dark/light mode
def load_css():
    # Get current theme
    is_dark = st.session_state.get('dark_mode', False)
    
    # Define CSS based on theme
    if is_dark:
        # Dark theme CSS
        css = """
        <style>
        /* Dark Theme */
        .main .block-container {
            background-color: #111827 !important;
            color: #f9fafb !important;
        }
        
        [data-testid="stAppViewContainer"] {
            background-color: #111827 !important;
            color: #f9fafb !important;
        }
        
        .stTextInput > div > div > input {
            background-color: #1f2937 !important;
            color: #f9fafb !important;
            border-color: #374151 !important;
        }
        
        .stCodeBlock {
            background-color: #1f2937 !important;
            border-color: #374151 !important;
        }
        
        .custom-card {
            background-color: #1f2937 !important;
            border-color: #374151 !important;
            color: #f9fafb !important;
        }
        
        .css-1d391kg {
            background-color: #1f2937 !important;
        }
        
        /* Header Styling */
        .main-header {
            background: linear-gradient(135deg, #60a5fa 0%, #3b82f6 100%);
            padding: 2rem 0;
            border-radius: 0 0 20px 20px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
        }
        
        .main-header h1 {
            color: white !important;
            font-size: 3rem !important;
            font-weight: 700 !important;
            text-align: center;
            margin-bottom: 0.5rem;
        }
        
        .main-header p {
            color: rgba(255, 255, 255, 0.9) !important;
            text-align: center;
            font-size: 1.2rem;
            margin: 0;
        }
        
        /* Card Styling */
        .custom-card {
            background: #1f2937 !important;
            border: 1px solid #374151 !important;
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease;
            color: #f9fafb !important;
        }
        
        .custom-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px -5px rgba(0, 0, 0, 0.15);
        }
        
        /* Button Styling */
        .stButton > button {
            border-radius: 8px !important;
            font-weight: 600 !important;
            padding: 0.75rem 1.5rem !important;
            transition: all 0.3s ease !important;
            border: none !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3) !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-1px) !important;
            box-shadow: 0 6px 20px -3px rgba(0, 0, 0, 0.2) !important;
        }
        
        /* Input Styling */
        .stTextInput > div > div > input {
            border-radius: 8px !important;
            border: 2px solid #374151 !important;
            padding: 0.75rem 1rem !important;
            font-size: 1rem !important;
            transition: all 0.3s ease !important;
            background: #1f2937 !important;
            color: #f9fafb !important;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #60a5fa !important;
            box-shadow: 0 0 0 3px rgba(96, 165, 250, 0.1) !important;
        }
        
        /* Success/Error Messages */
        .success-message {
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: white;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
        }
        
        .error-message {
            background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
            color: white;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
        }
        
        /* Footer Styling */
        .footer {
            text-align: center;
            padding: 2rem 0;
            color: #d1d5db;
            border-top: 1px solid #374151;
            margin-top: 3rem;
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .main-header h1 {
                font-size: 2rem !important;
            }
            
            .main-header p {
                font-size: 1rem;
            }
            
            .custom-card {
                padding: 1rem;
            }
        }
        </style>
        """
    else:
        # Light theme CSS
        css = """
        <style>
        /* Light Theme */
        .main .block-container {
            background-color: #ffffff !important;
            color: #1f2937 !important;
        }
        
        [data-testid="stAppViewContainer"] {
            background-color: #ffffff !important;
            color: #1f2937 !important;
        }
        
        .stTextInput > div > div > input {
            background-color: #ffffff !important;
            color: #1f2937 !important;
            border-color: #e5e7eb !important;
        }
        
        .stCodeBlock {
            background-color: #ffffff !important;
            border-color: #e5e7eb !important;
        }
        
        .custom-card {
            background-color: #ffffff !important;
            border-color: #e5e7eb !important;
            color: #1f2937 !important;
        }
        
        .css-1d391kg {
            background-color: #f8f9fa !important;
        }
        
        /* Header Styling */
        .main-header {
            background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
            padding: 2rem 0;
            border-radius: 0 0 20px 20px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        
        .main-header h1 {
            color: white !important;
            font-size: 3rem !important;
            font-weight: 700 !important;
            text-align: center;
            margin-bottom: 0.5rem;
        }
        
        .main-header p {
            color: rgba(255, 255, 255, 0.9) !important;
            text-align: center;
            font-size: 1.2rem;
            margin: 0;
        }
        
        /* Card Styling */
        .custom-card {
            background: #ffffff !important;
            border: 1px solid #e5e7eb !important;
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
            color: #1f2937 !important;
        }
        
        .custom-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px -5px rgba(0, 0, 0, 0.15);
        }
        
        /* Button Styling */
        .stButton > button {
            border-radius: 8px !important;
            font-weight: 600 !important;
            padding: 0.75rem 1.5rem !important;
            transition: all 0.3s ease !important;
            border: none !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-1px) !important;
            box-shadow: 0 6px 20px -3px rgba(0, 0, 0, 0.2) !important;
        }
        
        /* Input Styling */
        .stTextInput > div > div > input {
            border-radius: 8px !important;
            border: 2px solid #e5e7eb !important;
            padding: 0.75rem 1rem !important;
            font-size: 1rem !important;
            transition: all 0.3s ease !important;
            background: #ffffff !important;
            color: #1f2937 !important;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #3b82f6 !important;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
        }
        
        /* Success/Error Messages */
        .success-message {
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: white;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        
        .error-message {
            background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
            color: white;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        
        /* Footer Styling */
        .footer {
            text-align: center;
            padding: 2rem 0;
            color: #6b7280;
            border-top: 1px solid #e5e7eb;
            margin-top: 3rem;
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .main-header h1 {
                font-size: 2rem !important;
            }
            
            .main-header p {
                font-size: 1rem;
            }
            
            .custom-card {
                padding: 1rem;
            }
        }
        </style>
        """
    
    st.markdown(css, unsafe_allow_html=True)

def generate_readme(project_title):
    """Generate a professional README.md for the given project title."""
    
    prompt = f"""Generate a comprehensive, professional README.md file for a project titled "{project_title}". 

The README should include:
1. A compelling project title and description
2. Features section with 5-8 key features
3. Installation instructions with code blocks
4. Usage examples with code snippets
5. Contributing guidelines
6. License information (MIT License)
7. Badges for build status, version, etc.
8. Screenshots section (placeholder)
9. API documentation if applicable
10. Troubleshooting section

Make it production-ready and professional. Use proper markdown formatting with headers, code blocks, lists, and tables where appropriate. Include realistic but generic installation commands and usage examples. The tone should be professional yet approachable.

Return ONLY the markdown content, no additional text or explanations."""

    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": "You are an expert software documentation writer. Generate professional, production-ready README files."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=4000
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error generating README: {str(e)}")
        return None

def generate_prd(project_title):
    """Generate a detailed Product Requirements Document for the given project title."""
    
    prompt = f"""Generate a comprehensive Product Requirements Document (PRD) for a project titled "{project_title}". 

The PRD should include:

1. **Executive Summary**
   - Project overview and objectives
   - Key success metrics

2. **Product Vision**
   - Vision statement
   - Target audience/user personas
   - Value proposition

3. **Functional Requirements**
   - Core features and functionality
   - User stories and acceptance criteria
   - User flows and workflows

4. **Non-Functional Requirements**
   - Performance requirements
   - Security requirements
   - Scalability requirements
   - Usability requirements

5. **Technical Requirements**
   - Technology stack recommendations
   - Architecture considerations
   - Integration requirements

6. **User Experience**
   - UI/UX guidelines
   - Accessibility requirements
   - Mobile responsiveness

7. **Success Metrics**
   - KPIs and measurement criteria
   - Analytics requirements

8. **Timeline and Milestones**
   - Development phases
   - Key milestones
   - Release strategy

9. **Risk Assessment**
   - Technical risks
   - Business risks
   - Mitigation strategies

10. **Appendix**
    - Glossary of terms
    - References and resources

Make it professional, detailed, and actionable. Use clear headings, bullet points, and structured formatting. The document should be comprehensive enough for development teams to execute on.

Return ONLY the document content, no additional text or explanations."""

    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": "You are an expert product manager and technical writer. Generate comprehensive, professional PRDs."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=6000
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error generating PRD: {str(e)}")
        return None

def main():
    # Load custom CSS
    load_css()
    
    # Initialize session state for theme
    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = False
    
    # Theme toggle
    col1, col2, col3 = st.columns([1, 1, 1])
    with col3:
        if st.button("🌙" if not st.session_state.dark_mode else "☀️", key="theme_toggle"):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.experimental_rerun()
    
    # Header with gradient background
    st.markdown("""
    <div class="main-header">
        <h1>📄 AutoDoc AI</h1>
        <p>Automatically generate professional software documentation from your project title</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar with enhanced styling
    with st.sidebar:
        st.markdown("""
        <div class="custom-card">
            <h3>⚙️ Settings</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.info("🚀 Powered by Groq API with Llama3-70b-8192")
        
        st.markdown("""
        <div class="custom-card">
            <h4>✨ Features</h4>
            <ul>
                <li>Generate professional README.md files</li>
                <li>Create detailed Product Requirements Documents</li>
                <li>Download results as .md or .txt files</li>
                <li>Fast AI-powered generation</li>
                <li>Dark/Light mode support</li>
                <li>Responsive design</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="custom-card">
            <h4>🎯 How it works</h4>
            <ol>
                <li>Enter your project title</li>
                <li>Choose README or PRD generation</li>
                <li>Get professional documentation instantly</li>
                <li>Download and use in your projects</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="custom-card">
            <h2>🚀 Generate Documentation</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Project title input with enhanced styling
        project_title = st.text_input(
            "Enter your project title:",
            placeholder="e.g., TaskMaster - AI-Powered Task Management System",
            help="Provide a descriptive title for your project"
        )
        
        if project_title:
            st.markdown(f"""
            <div class="success-message">
                <strong>Project:</strong> {project_title}
            </div>
            """, unsafe_allow_html=True)
            
            # Generation buttons with enhanced styling
            col_btn1, col_btn2 = st.columns(2)
            
            with col_btn1:
                if st.button("📖 Generate README.md", type="primary", use_container_width=True):
                    with st.spinner("🔄 Generating professional README..."):
                        readme_content = generate_readme(project_title)
                        if readme_content:
                            st.session_state.readme_content = readme_content
                            st.session_state.show_readme = True
                            st.session_state.show_prd = False
                            st.success("✅ README generated successfully!")
            
            with col_btn2:
                if st.button("📋 Generate PRD", type="secondary", use_container_width=True):
                    with st.spinner("🔄 Generating comprehensive PRD..."):
                        prd_content = generate_prd(project_title)
                        if prd_content:
                            st.session_state.prd_content = prd_content
                            st.session_state.show_prd = True
                            st.session_state.show_readme = False
                            st.success("✅ PRD generated successfully!")
    
    with col2:
        st.markdown("""
        <div class="custom-card">
            <h3>📊 Quick Stats</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.metric("API Model", "Llama3-70b")
        st.metric("Max Tokens", "8,192")
        st.metric("Generation Speed", "~2-5s")
        
        st.markdown("""
        <div class="custom-card">
            <h4>💡 Tips</h4>
            <ul>
                <li>Be specific with your project title</li>
                <li>Include key technologies in the title</li>
                <li>Mention target audience if relevant</li>
                <li>Use descriptive names for better results</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Display generated content with enhanced styling
    if hasattr(st.session_state, 'show_readme') and st.session_state.show_readme:
        st.markdown("---")
        st.markdown("""
        <div class="custom-card">
            <h2>📖 Generated README.md</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Download buttons with enhanced styling
        col_dl1, col_dl2 = st.columns(2)
        with col_dl1:
            st.download_button(
                label="📥 Download README.md",
                data=st.session_state.readme_content,
                file_name=f"README_{project_title.replace(' ', '_')}.md",
                mime="text/markdown",
                use_container_width=True
            )
        with col_dl2:
            st.download_button(
                label="📥 Download as .txt",
                data=st.session_state.readme_content,
                file_name=f"README_{project_title.replace(' ', '_')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        # Display content with enhanced styling
        st.markdown("### Preview:")
        st.code(st.session_state.readme_content, language="markdown")
    
    if hasattr(st.session_state, 'show_prd') and st.session_state.show_prd:
        st.markdown("---")
        st.markdown("""
        <div class="custom-card">
            <h2>📋 Generated Product Requirements Document</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Download buttons with enhanced styling
        col_dl1, col_dl2 = st.columns(2)
        with col_dl1:
            st.download_button(
                label="📥 Download PRD.md",
                data=st.session_state.prd_content,
                file_name=f"PRD_{project_title.replace(' ', '_')}.md",
                mime="text/markdown",
                use_container_width=True
            )
        with col_dl2:
            st.download_button(
                label="📥 Download as .txt",
                data=st.session_state.prd_content,
                file_name=f"PRD_{project_title.replace(' ', '_')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        # Display content with enhanced styling
        st.markdown("### Preview:")
        st.code(st.session_state.prd_content, language="markdown")
    
    # Enhanced footer
    st.markdown("""
    <div class="footer">
        <p>Built with ❤️ using Streamlit and Groq API</p>
        <p>AutoDoc AI - Making documentation effortless</p>
        <p>Theme: """ + ("Dark" if st.session_state.dark_mode else "Light") + """ Mode</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":

    main() 
