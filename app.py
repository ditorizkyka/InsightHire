import streamlit as st
from parser.parser_jd import parse_jd
from parser.parser_resume import parse_resume
from matcher.matcher import match_resume
from scorer.scorer import score_resume
import tempfile
import fitz  # PyMuPDF

st.set_page_config(page_title="InsightHire", layout="centered")
st.title("📄 InsightHire – AI Resume Screener")

st.markdown("Upload resume kamu dan masukkan Job Description untuk melihat tingkat kecocokan.")

# Upload Resume
resume_file = st.file_uploader("Upload CV/Resume (.pdf)", type=["pdf"])

# Dropdown Job Options
job_options = [
    "Pilih Job Role...",
    "Software Engineer",
    "Data Analyst",
    "UI/UX Designer",
    "Product Manager",
    "Digital Marketer",
    "Machine Learning Engineer",
    "Backend Developer",
    "Frontend Developer",
    "DevOps Engineer",
]
selected_job = st.selectbox("Atau pilih salah satu Job Role populer:", job_options)

# Contoh deskripsi kerja otomatis (bisa kamu sesuaikan atau buat dictionary khusus)
set_skills = {
    "Software Engineer": [
        # Bahasa Pemrograman
        "Python", "Java", "C++", "JavaScript", "TypeScript", "Dart", "Kotlin", "Swift", "Go", "C#", "PHP", "Ruby",
    
        # Paradigma & Praktik Pengembangan
        "Object-Oriented Programming (OOP)", "Functional Programming", "Test-Driven Development (TDD)", 
        "Agile", "Scrum", "SDLC", "CI/CD", "Clean Architecture", "SOLID Principles", "Design Patterns",
    
        # Version Control & Tools
        "Git", "GitHub", "GitLab", "Bitbucket", "Docker", "Postman", "Jira", "VS Code", "Android Studio", "Xcode",
    
        # Frontend Development
        "HTML", "CSS", "JavaScript", "TypeScript", "React", "Vue.js", "Angular", "Tailwind CSS", "Bootstrap",
        "Next.js", "Nuxt.js", "Redux", "Responsive Design", "Progressive Web Apps (PWA)",
    
        # Backend Development
        "Node.js", "Express.js", "Spring Boot", "Django", "Flask", "Laravel", "FastAPI", "Ruby on Rails",
        "REST API", "GraphQL", "gRPC", "Authentication & Authorization", "Microservices Architecture",
    
        # Database & Storage
        "MySQL", "PostgreSQL", "MongoDB", "Firebase", "SQLite", "Redis", "NoSQL", "SQL", "ORM",
    
        # Mobile Development
        "Flutter", "React Native", "Android", "iOS", "SwiftUI", "Jetpack Compose", "Mobile UI/UX Design",
        "Mobile App Deployment", "Play Store", "App Store", "Mobile Programmer", "Mobile Developer",
    
        # DevOps & Infrastructure
        "Docker", "Kubernetes", "NGINX", "Apache", "AWS", "Google Cloud Platform", "Firebase", "Heroku", "Netlify", "Vercel",
    
        # Testing & Debugging
        "Unit Testing", "Integration Testing", "UI Testing", "Mockito", "JUnit", "Espresso", "Debugging Tools",
    
        # Soft Skills & Engineering Mindset
        "Problem Solving", "System Design", "Team Collaboration", "Code Review", "Mentorship", "Documentation Writing"
    ],

    "Data Analyst": [
        "SQL", "Excel", "Tableau", "Power BI", "Data Cleaning", "Python",
        "Pandas", "Statistics", "Data Visualization", "Business Intelligence"
    ],
    "UI/UX Designer": [
        "Figma", "Adobe XD", "User Research", "Wireframing", "Prototyping",
        "Design Thinking", "Sketch", "UI Design", "UX Writing", "Usability Testing"
    ],
    "Product Manager": [
        "Product Management", "Agile", "Scrum", "Market Research", "Roadmapping",
        "JIRA", "Stakeholder Management", "User Stories", "Analytics", "Business Strategy"
    ],
    "Digital Marketer": [
        "SEO", "SEM", "Google Ads", "Facebook Ads", "Content Marketing",
        "Email Marketing", "Google Analytics", "Copywriting", "Marketing Strategy", "Social Media"
    ],
    "Machine Learning Engineer": [
        # Bahasa dan Library
        "Python", "R", "TensorFlow", "PyTorch", "Scikit-learn", "Pandas", "NumPy", "Matplotlib", "Seaborn", "OpenCV",
        
        # Platform & Frameworks
        "Huggingface Transformers", "Keras", "XGBoost", "LightGBM", "ONNX", "FastAI", "MLflow",
        
        # Tools & Environment
        "Jupyter", "Google Colab", "Docker", "Git", "VS Code", "Conda", "Weights & Biases", "DVC",
        
        # Cloud & Deployment
        "Model Deployment", "Flask API", "FastAPI", "AWS SageMaker", "GCP Vertex AI", "Azure ML",
        "Streamlit", "Gradio", "Heroku", "Render",
        
        # Machine Learning Concepts
        "Supervised Learning", "Unsupervised Learning", "Reinforcement Learning", "Deep Learning",
        "Transfer Learning", "Model Evaluation", "Hyperparameter Tuning", "Cross Validation",
        "Overfitting/Underfitting", "Feature Engineering", "Dimensionality Reduction",
        
        # NLP & CV
        "Natural Language Processing", "Transformers", "Text Classification", "NER", "Topic Modeling",
        "Computer Vision", "Image Classification", "Object Detection", "OCR",
        
        # Data Engineering & Processing
        "Data Preprocessing", "Data Cleaning", "ETL Pipelines", "SQL", "BigQuery", "Spark (PySpark)",
        
        # MLOps & CI/CD
        "CI/CD for ML", "MLOps", "Pipeline Automation", "Monitoring ML Models", "Version Control for Models"
    ],

    "Backend Developer": [
        "Node.js", "Django", "Flask", "Java", "SQL", "REST API",
        "Authentication", "Database Design", "Docker", "Git"
    ],
    "Frontend Developer": [
        "HTML", "CSS", "JavaScript", "React", "Vue.js", "Responsive Design",
        "Tailwind CSS", "Redux", "UI Frameworks", "Cross-browser Compatibility"
    ],
    "DevOps Engineer": [
        "Docker", "Kubernetes", "CI/CD", "AWS", "Azure", "Terraform",
        "Linux", "Bash", "Monitoring", "GitOps", "Ansible", "Jenkins"
    ],
}

# WRITE JOB DESCRIPTION
jd_text = st.text_area("Paste Job Description", height=250)

# Validasi input dan proses
if st.button("🔍 Analyze Resume"):
    if not resume_file or not jd_text.strip():
        st.warning("Silakan upload resume dan isi job description.")
    else:
        with st.spinner("🔎 Menganalisis resume..."):
    
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                tmp.write(resume_file.read())
                resume_path = tmp.name

            with fitz.open(resume_path) as doc:
                resume_text = "".join(page.get_text() for page in doc)

            preprocessed_resume = parse_resume(resume_text)
            preprocessed_jd = parse_jd(jd_text)
            similarity, matched, missing = match_resume(preprocessed_jd, preprocessed_resume, set_skills[selected_job])
            result = score_resume(similarity, matched, missing)

            st.success("✅ Analisis selesai!")
            st.subheader("📊 Resume Fit Score:")
            st.progress(min(result["score"] / 100, 1.0))
            st.metric(label="Skor Kecocokan", value=f"{result['score']}%")

            st.subheader("✅ Skill yang Terpenuhi")
            if not result["matched"]:
                st.write("Tidak ada skill yang match dengan Job Description yang anda berikan")
            else :
                st.write(", ".join(result["matched"]) or "-")
            

            st.subheader("❌ Skill yang Kurang")
            if not missing:
                st.write("Tidak ada skill yang miss dengan Job Description yang anda berikan. Congrats")
            else :
                st.write(", ".join(missing) or "-")
                

            st.subheader("💬 Feedback")
            st.info(result["feedback"])
