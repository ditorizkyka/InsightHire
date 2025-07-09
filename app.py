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
    "AI/ML Engineer",
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
        # Pengolahan & Query Data
        "SQL", "NoSQL", "MongoDB", "MySQL", "PostgreSQL",
    
        # Bahasa Pemrograman & Libraries
        "Python", "R", "Pandas", "NumPy", "Matplotlib", "Seaborn", "Scikit-learn",
    
        # Data Wrangling & Cleaning
        "Data Cleaning", "Data Wrangling", "Missing Data Handling", "Outlier Detection",
    
        # Visualisasi Data
        "Tableau", "Power BI", "Looker", "Google Data Studio", "Data Visualization",
    
        # Alat Spreadsheet & BI Tools
        "Excel (PivotTable, VLOOKUP, Macro)", "Google Sheets", "Business Intelligence",
    
        # Statistik & Analisis
        "Descriptive Statistics", "Inferential Statistics", "A/B Testing", "Hypothesis Testing",
        "Regression Analysis", "Probability Theory", "Time Series Analysis",
    
        # ETL & Data Pipeline
        "ETL Processes", "Apache Airflow", "Data Pipeline Design",
    
        # Cloud & Big Data Tools
        "Google BigQuery", "Amazon Redshift", "Azure Data Lake", "Snowflake", "Hadoop", "Spark",
    
        # Tools & Workflow
        "Jupyter Notebook", "VS Code", "Git", "GitHub", "Docker (basic)", "Command Line (CLI)",
    
        # Soft Skills & Business Acumen
        "Critical Thinking", "Problem Solving", "Communication Skills", "Domain Knowledge", "Stakeholder Management",
    
        # Bonus/Advanced (optional)
        "Machine Learning (Basic)", "Deep Dive Cohort Analysis", "Churn Prediction", "Dashboard Design Principles"
    ],
    "UI/UX Designer": [
        # Desain Tools & Prototyping
        "Figma", "Adobe XD", "Sketch", "InVision", "Framer", "Marvel", "Axure RP", "Balsamiq",
    
        # UI Design
        "Visual Design", "Typography", "Color Theory", "Layout Design", "Design Systems", "Component-based Design",
        "Responsive Design", "Mobile-first Design", "Accessibility (WCAG)", "Atomic Design",
    
        # UX Design
        "User Research", "User Persona", "Empathy Mapping", "Customer Journey Mapping", 
        "Information Architecture", "Interaction Design", "User Flows", "Wireframing", "Low-Fidelity Prototyping",
        "High-Fidelity Prototyping", "UX Writing", "Usability Testing", "A/B Testing", "Task Analysis",
    
        # Metodologi & Proses
        "Design Thinking", "Agile UX", "Lean UX", "Double Diamond", "Human-Centered Design", 
        "Heuristic Evaluation", "Card Sorting", "Storyboarding",
    
        # Kolaborasi & Tools Pendukung
        "Zeplin", "FigJam", "Notion", "Miro", "Jira", "Confluence", "Slack", "Trello", "Google Workspace",
    
        # Coding Awareness (Opsional untuk kolaborasi dengan dev)
        "HTML", "CSS", "JavaScript (Basic)", "Component Handoff", "Responsive Grid System",
    
        # Soft Skills
        "Problem Solving", "Empathy", "Creativity", "Communication", "Collaboration", "Presentation Skills",
    
        # Bonus / Advanced
        "Design for AR/VR", "Motion Design", "Design Tokens", "Voice UI Design", 
        "Microinteraction Design", "UX Metrics & Analytics", "UX for AI Interfaces"
    ],

   "Product Manager": [
        # Core Product Management
        "Product Management", "Product Lifecycle Management", "Product Discovery", 
        "Product Strategy", "MVP Definition", "Product Roadmapping", "Product Analytics",
    
        # Agile & Project Management
        "Agile", "Scrum", "Kanban", "Sprint Planning", "Backlog Grooming", 
        "User Stories", "Epics", "Acceptance Criteria", "Release Planning",
    
        # Tools & Platforms
        "JIRA", "Confluence", "Trello", "Notion", "Asana", "Miro", "Figma (for collaboration)",
        "Productboard", "Aha!", "ClickUp",
    
        # Research & Validation
        "Market Research", "Competitive Analysis", "Customer Interviews", "Surveys",
        "Usability Testing", "Problem Framing", "Design Sprint",
    
        # Business & Strategy
        "Business Strategy", "Go-To-Market Strategy", "Pricing Strategy", 
        "Revenue Models", "KPI Definition", "Product-Market Fit", "OKRs", "Unit Economics",
    
        # Data & Analytics
        "Analytics", "A/B Testing", "Cohort Analysis", "Conversion Funnel Analysis", 
        "Google Analytics", "Mixpanel", "Amplitude", "SQL (Basic)",
    
        # Stakeholder & Team Management
        "Stakeholder Management", "Cross-functional Collaboration", 
        "Team Alignment", "Communication Skills", "Presentation Skills",
    
        # UX/Tech Awareness
        "Customer Journey Mapping", "Basic UX/UI Knowledge", "Technical Understanding",
        "APIs (Basic Understanding)", "System Thinking",
    
        # Soft Skills
        "Leadership", "Empathy", "Critical Thinking", "Problem Solving", "Prioritization", 
        "Decision Making", "Conflict Resolution",
    
        # Bonus / Emerging Areas
        "AI Product Management", "SaaS Product Management", "Growth Product Management",
        "Design Thinking", "Jobs-To-Be-Done (JTBD)", "Lean Startup"
    ],

    "Digital Marketer": [
        # Core Channels & Platforms
        "SEO", "SEM", "Google Ads", "Facebook Ads", "Instagram Ads", "LinkedIn Ads",
        "Twitter Ads", "YouTube Marketing", "TikTok Ads", "Programmatic Advertising",
    
        # Analytics & Optimization
        "Google Analytics", "Google Tag Manager", "UTM Tracking", "A/B Testing", 
        "Conversion Rate Optimization (CRO)", "Funnel Analysis", "Data-Driven Marketing",
        "Marketing Attribution", "Customer Journey Mapping",
    
        # Content & Engagement
        "Content Marketing", "Copywriting", "Content Strategy", "Blog Writing",
        "Video Marketing", "Content Calendar Management", "Storytelling", "Content SEO",
        
        # Email & Automation
        "Email Marketing", "Marketing Automation", "Lead Nurturing", "Drip Campaigns",
        "Tools like Mailchimp, HubSpot, Klaviyo", "CRM Integration",
    
        # Social Media
        "Social Media Strategy", "Social Media Management", "Community Management",
        "Influencer Marketing", "Social Listening", "Brand Voice Development",
    
        # Strategy & Planning
        "Marketing Strategy", "Digital Marketing Strategy", "Campaign Planning", 
        "Competitor Analysis", "Market Research", "Customer Segmentation",
        "Buyer Persona Development", "Positioning & Messaging",
    
        # Tools & Platforms
        "Google Search Console", "Ahrefs", "SEMrush", "Moz", "Hootsuite", "Buffer",
        "Canva", "Figma (for creatives)", "Meta Business Suite", "HubSpot", "Zapier",
    
        # Paid Media & Performance
        "Pay-per-click (PPC)", "Retargeting", "Display Advertising", 
        "Affiliate Marketing", "Cost-per-click (CPC)", "ROI/ROAS Optimization",
    
        # Soft Skills
        "Creative Thinking", "Analytical Thinking", "Project Management", 
        "Collaboration", "Communication Skills", "Adaptability",
    
        # Bonus / Advanced
        "Growth Marketing", "Viral Marketing", "Guerrilla Marketing", 
        "Web3 Marketing", "AI in Marketing", "Neuromarketing"
    ],

    "AI/ML Engineer": [
        # Bahasa dan Library
        "Python", "R", "TensorFlow", "PyTorch", "Scikit-learn", "Pandas", "NumPy", "Matplotlib", "Seaborn", "OpenCV",
        
        # Platform & Frameworks
        "Huggingface Transformers", "Keras", "XGBoost", "LightGBM", "ONNX", "FastAI", "MLflow",
        
        # Tools & Environment
        "Jupyter", "Google Colab", "Docker", "Git", "VS Code", "Conda", "Weights & Biases", "DVC",
        
        # Cloud & Deployment
        "Model Deployment", "Flask API", "FastAPI", "AWS SageMaker", "GCP Vertex AI", "Azure ML","Artificial Intelligence"
        "Streamlit", "Gradio", "Heroku", "Render", "AWS", "Azure", "GCP",
        
        # Machine Learning Concepts
        "Supervised Learning", "Unsupervised Learning", "Reinforcement Learning", "Deep Learning",
        "Transfer Learning", "Model Evaluation", "Hyperparameter Tuning", "Cross Validation",
        "Overfitting/Underfitting", "Feature Engineering", "Dimensionality Reduction","Information Retrieval", "Recommender System", "LLM",
        
        # NLP & CV
        "Natural Language Processing", "Transformers", "Text Classification", "NER", "Topic Modeling",
        "Computer Vision", "Image Classification", "Object Detection", "OCR",
        
        # Data Engineering & Processing
        "Data Preprocessing", "Data Cleaning", "ETL Pipelines", "SQL", "BigQuery", "Spark (PySpark)",
        
        # MLOps & CI/CD
        "CI/CD for ML", "MLOps", "Pipeline Automation", "Monitoring ML Models", "Version Control for Models"
    ],

    "Backend Developer": [
        # Bahasa Pemrograman
        "Java", "Python", "Node.js", "Go", "Ruby", "PHP", "C#", "Kotlin",
    
        # Framework Backend
        "Django", "Flask", "Express.js", "Spring Boot", "FastAPI", "Laravel", "ASP.NET",
    
        # API & Komunikasi Data
        "REST API", "GraphQL", "gRPC", "WebSocket", "API Versioning", "OpenAPI/Swagger",
    
        # Database
        "SQL", "PostgreSQL", "MySQL", "SQLite", "Oracle", 
        "NoSQL", "MongoDB", "Redis", "Firebase", "Cassandra",
    
        # Database Design & Optimization
        "Database Design", "Normalization", "Indexing", "Query Optimization",
        "Data Modeling", "ERD (Entity Relationship Diagram)",
    
        # Keamanan
        "Authentication", "Authorization", "JWT", "OAuth2", "Rate Limiting", 
        "Input Validation", "CORS", "Encryption", "OWASP Best Practices",
    
        # DevOps & Deployment
        "Docker", "Kubernetes (basic)", "CI/CD", "Nginx", "Apache", 
        "Cloud Platforms (AWS, GCP, Azure)", "Heroku", "Render", "Railway",
    
        # Testing & Debugging
        "Unit Testing", "Integration Testing", "Postman", "Pytest", "Jest", 
        "Logging", "Monitoring", "Error Handling", "Load Testing",
    
        # Tools & Workflow
        "Git", "GitHub", "GitLab", "Bitbucket", "VS Code", "Command Line", 
        "Agile / Scrum", "JIRA", "Notion",
    
        # Software Architecture & Design
        "MVC", "MVVM", "Microservices", "Monolith", "Clean Architecture", 
        "Event-driven Architecture", "Message Queues (RabbitMQ, Kafka)",
    
        # Soft Skills
        "Problem Solving", "System Design", "Debugging", "Collaboration", 
        "Code Review", "Documentation",
    
        # Bonus / Advanced
        "Serverless", "Load Balancing", "Caching Strategies", 
        "Multithreading", "Asynchronous Programming", "Webhooks"
    ],

    "Frontend Developer": [
        # Core Web Technologies
        "HTML", "CSS", "JavaScript", "TypeScript", "DOM Manipulation", "ES6+ Features",
    
        # Frameworks & Libraries
        "React", "Vue.js", "Angular", "Next.js", "Nuxt.js", "Svelte", "jQuery",
    
        # State Management
        "Redux", "Zustand", "Recoil", "MobX", "Pinia", "Context API",
    
        # Styling Tools
        "Tailwind CSS", "SASS/SCSS", "Styled-components", "Emotion", "CSS Modules", "Bootstrap", "Material UI", "Chakra UI",
    
        # Responsive & Cross-browser
        "Responsive Design", "Media Queries", "Flexbox", "Grid Layout", 
        "Cross-browser Compatibility", "Mobile-first Design", "Accessibility (WCAG)",
    
        # Build Tools & Bundlers
        "Webpack", "Vite", "Parcel", "Babel", "ESLint", "Prettier",
    
        # Testing
        "Jest", "React Testing Library", "Cypress", "Playwright", "Mocha", "Storybook",
    
        # Version Control & Workflow
        "Git", "GitHub", "Bitbucket", "CI/CD Integration", "Code Review", "Agile/Scrum",
    
        # Performance & Optimization
        "Code Splitting", "Lazy Loading", "Image Optimization", "Web Vitals", "Caching", "Service Workers",
    
        # API Integration & Data Handling
        "REST API", "GraphQL", "Axios", "Fetch API", "WebSocket", "Form Handling & Validation",
    
        # Browser & Tools
        "Chrome DevTools", "Postman", "Lighthouse", "Figma (for dev handoff)", "Notion", "JIRA",
    
        # Advanced Topics
        "Progressive Web Apps (PWA)", "Static Site Generation (SSG)", "Server Side Rendering (SSR)", 
        "Internationalization (i18n)", "Accessibility Auditing", "Animations (Framer Motion, GSAP)",
    
        # Soft Skills
        "Collaboration", "Communication", "Attention to Detail", "Problem Solving", "UI/UX Awareness"
    ],

    "DevOps Engineer": [
        # Core Concepts
        "DevOps Practices", "CI/CD", "Infrastructure as Code (IaC)", "GitOps", 
        "Automation", "Monitoring", "Observability", "High Availability",
    
        # Containerization & Orchestration
        "Docker", "Docker Compose", "Kubernetes", "Helm", "Kustomize", "Podman",
    
        # Cloud Platforms
        "AWS (EC2, S3, EKS, Lambda)", "Azure (AKS, App Services, Pipelines)", 
        "Google Cloud Platform (GCP)", "DigitalOcean", "Cloudflare",
    
        # IaC & Configuration Management
        "Terraform", "CloudFormation", "Pulumi", "Ansible", "Chef", "SaltStack", "Packer",
    
        # CI/CD Tools
        "Jenkins", "GitHub Actions", "GitLab CI/CD", "CircleCI", "Travis CI", "ArgoCD", "Spinnaker",
    
        # Scripting & Programming
        "Bash", "Shell Scripting", "Python", "Groovy (for Jenkinsfiles)", "YAML", "Go (optional)",
    
        # Operating Systems & Environments
        "Linux", "Ubuntu", "CentOS", "RHEL", "Systemd", "Networking Fundamentals",
    
        # Source Control & Versioning
        "Git", "GitHub", "GitLab", "Bitbucket", "Branching Strategies", "Merge Requests / PRs",
    
        # Monitoring & Logging
        "Prometheus", "Grafana", "ELK Stack (Elasticsearch, Logstash, Kibana)", 
        "EFK Stack", "Datadog", "New Relic", "Sentry", "Fluentd", "Nagios", "Zabbix",
    
        # Security & Compliance
        "Secrets Management (Vault, AWS Secrets Manager)", 
        "SSL/TLS", "IAM Roles/Policies", "Container Security", 
        "DevSecOps", "Security Scanning (Trivy, Snyk)",
    
        # Deployment & Release Strategies
        "Blue-Green Deployment", "Canary Deployment", "Rolling Updates", "Feature Flags",
    
        # Soft Skills
        "Problem Solving", "Incident Management", "Collaboration", 
        "Communication", "Documentation", "Agile/Scrum", "Root Cause Analysis",
    
        # Bonus / Advanced
        "Service Mesh (Istio, Linkerd)", "Serverless DevOps", "Site Reliability Engineering (SRE)",
        "Edge Computing", "Chaos Engineering", "Performance Tuning"
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
            result = score_resume(similarity, matched, missing, selected_job)

            st.success("✅ Analisis selesai!")
            st.subheader("📊 Resume Fit Score:")
            st.progress(min(result["score"] / 100, 1.0))
            st.metric(label="Skor Kecocokan", value=f"{result['score']}%")

            st.subheader("✅ Skill yang Terpenuhi")
            if not result["matched"]:
                st.write("😅 Sepertinya belum ada skill di CV-mu yang cocok dengan job description ini. Yuk, coba tambahkan beberapa skill yang relevan biar makin klop! 💪✨")
            else :
                st.write("Skill yang sudah ada di CV mu adalah " + (", ".join(result["matched"]) or "-"))

        
            st.subheader("❌ Skill yang Kurang")
            if not result["matched"] and not result["missing"]:
                 st.write("🤔 Hmm... Sepertinya isi CV-mu belum sesuai dengan job description ini. Yuk, coba sesuaikan atau tambahkan skill yang relevan biar lebih match! 💡📄")
            elif not result["missing"]:
                st.write("🎉 Keren! Semua skill di CV-mu sudah sesuai dengan job description yang diberikan. Nggak ada yang miss — great job! 💼🔥")
            else :
                st.write("Skill yang kurang di CV mu adalah " + (", ".join(result["missing"]) or "-"))

                

            st.subheader("💬 Feedback")
            st.info(result["feedback"])
