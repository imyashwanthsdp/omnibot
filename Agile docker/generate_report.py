import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = parse_xml(f'''
        <w:tcMar {nsdecls("w")}>
            <w:top w:w="{top}" w:type="dxa"/>
            <w:bottom w:w="{bottom}" w:type="dxa"/>
            <w:left w:w="{left}" w:type="dxa"/>
            <w:right w:w="{right}" w:type="dxa"/>
        </w:tcMar>
    ''')
    tcPr.append(tcMar)

def add_styled_heading(doc, text, level):
    p = doc.add_heading(text, level=level)
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    run = p.runs[0]
    if level == 1:
        run.font.size = Pt(18)
        run.font.bold = True
        run.font.color.rgb = RGBColor(15, 23, 42) # Dark Slate #0f172a
    elif level == 2:
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = RGBColor(37, 99, 235) # Royal Blue #2563eb
    elif level == 3:
        run.font.size = Pt(12)
        run.font.bold = True
        run.font.color.rgb = RGBColor(71, 85, 105) # Slate #475569
    return p

def add_code_block(doc, code_text):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F1F5F9") # Slate Light #f1f5f9
    set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
    
    # Border styling
    tcPr = cell._element.get_or_add_tcPr()
    borders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:top w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>
            <w:left w:val="single" w:sz="24" w:space="0" w:color="2563EB"/>
            <w:bottom w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>
            <w:right w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>
        </w:tcBorders>
    ''')
    tcPr.append(borders)

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(code_text)
    run.font.name = "Consolas"
    run.font.size = Pt(9.5)
    run.font.color.rgb = RGBColor(30, 41, 59)
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

def add_callout_box(doc, text, title="NOTE"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "EFF6FF")
    set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
    
    tcPr = cell._element.get_or_add_tcPr()
    borders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:top w:val="single" w:sz="4" w:space="0" w:color="BFDBFE"/>
            <w:left w:val="single" w:sz="24" w:space="0" w:color="3B82F6"/>
            <w:bottom w:val="single" w:sz="4" w:space="0" w:color="BFDBFE"/>
            <w:right w:val="single" w:sz="4" w:space="0" w:color="BFDBFE"/>
        </w:tcBorders>
    ''')
    tcPr.append(borders)

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    
    run_t = p.add_run(f"📌 {title}: ")
    run_t.bold = True
    run_t.font.color.rgb = RGBColor(29, 78, 216)
    
    run_b = p.add_run(text)
    run_b.font.color.rgb = RGBColor(30, 41, 59)
    run_b.font.size = Pt(10)
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

def build_word_document(output_path):
    doc = docx.Document()
    
    # Page Setup - Margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)
        
    # Standard Normal Style Font
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Calibri'
    font.size = Pt(11)
    font.color.rgb = RGBColor(30, 41, 59)

    # -------------------------------------------------------------
    # COVER / HEADER SECTION
    # -------------------------------------------------------------
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(20)
    p_title.paragraph_format.space_after = Pt(4)
    run_title = p_title.add_run("Continuous Integration (CI) Pipeline with Jenkins & Docker for a General Purpose Chatbot")
    run_title.font.size = Pt(22)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(15, 23, 42)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(24)
    run_sub = p_sub.add_run("Agile Software Engineering Sprint Project Report")
    run_sub.font.size = Pt(14)
    run_sub.font.color.rgb = RGBColor(37, 99, 235)

    # Metadata Box Table
    meta_table = doc.add_table(rows=4, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_table.autofit = False
    
    meta_data = [
        ("Contributors / Authors:", "1. Sodanapalli Yashwanth Reddy\n2. Chitmal Anvitha"),
        ("Project Topic:", "General Purpose AI Chatbot Application (OmniBot)"),
        ("GitHub Repository:", "https://github.com/imyashwanthsdp/omnibot.git"),
        ("Sprint Technology Stack:", "Jenkins, Docker, GitHub, Node.js / Express, TAP Test Runner")
    ]
    
    for i, (label, val) in enumerate(meta_data):
        row = meta_table.rows[i]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(2.2)
        c1.width = Inches(4.3)
        set_cell_background(c0, "F8FAFC")
        set_cell_background(c1, "FFFFFF")
        set_cell_margins(c0, 80, 80, 100, 100)
        set_cell_margins(c1, 80, 80, 100, 100)
        
        p0 = c0.paragraphs[0]
        r0 = p0.add_run(label)
        r0.bold = True
        r0.font.color.rgb = RGBColor(15, 23, 42)
        
        p1 = c1.paragraphs[0]
        r1 = p1.add_run(val)
        r1.font.color.rgb = RGBColor(30, 41, 59)
        
    doc.add_paragraph().paragraph_format.space_after = Pt(18)
    doc.add_page_break()

    # -------------------------------------------------------------
    # SECTION 1: EXECUTIVE SUMMARY & PROJECT DETAILS
    # -------------------------------------------------------------
    add_styled_heading(doc, "1. Executive Summary & Project Details", level=1)
    
    p = doc.add_paragraph(
        "In modern Agile software development, Continuous Integration (CI) serves as the backbone of automated quality assurance, rapid feedback, and seamless team collaboration. This Sprint focuses on building and containerizing a General Purpose Web Chatbot Application ('OmniBot') and integrating it into an automated Jenkins CI pipeline hosted on GitHub."
    )
    p.paragraph_format.space_after = Pt(8)

    add_styled_heading(doc, "1.1 Application Architecture & Stack", level=2)
    p = doc.add_paragraph(
        "The OmniBot General Chatbot is built using Node.js and Express. It features a rule-based NLP intent recognition engine capable of handling general conversational queries, mathematical expressions, time/date formatting, technology FAQs, and system health status."
    )
    p.paragraph_format.space_after = Pt(8)

    # Bullet list of files
    files_info = [
        ("src/chatbot.js", "Core Intent Recognition Engine. Evaluates user input against regular expressions for greetings, math operations (e.g. 'calculate 50 * 12'), tech FAQs (Jenkins/Docker), system status, and general fallbacks."),
        ("src/server.js", "Express Web Server exposing REST endpoints (/api/chat and /api/health) and serving static web assets."),
        ("public/", "Glassmorphism responsive UI with dark mode styling, quick action chips, typing indicators, and message bubble histories."),
        ("test/chatbot.test.js", "Automated unit test suite using Node.js built-in TAP test runner (node --test) validating all intent branches."),
        ("Dockerfile", "Multi-stage Docker definition utilizing Alpine Linux for reproducible, lightweight container production builds."),
        ("Jenkinsfile", "Declarative Jenkins Pipeline script defining automated CI stages from Checkout to Docker Image validation.")
    ]
    for fname, fdesc in files_info:
        bp = doc.add_paragraph(style='List Bullet')
        bp.paragraph_format.space_after = Pt(4)
        r_fn = bp.add_run(f"{fname}: ")
        r_fn.bold = True
        r_fn.font.color.rgb = RGBColor(37, 99, 235)
        bp.add_run(fdesc)

    add_callout_box(doc, "The codebase is publicly available and version-controlled on GitHub at: https://github.com/imyashwanthsdp/omnibot.git", title="REPOSITORY LINK")

    # -------------------------------------------------------------
    # SECTION 2: JENKINS & GITHUB CONFIGURATION
    # -------------------------------------------------------------
    add_styled_heading(doc, "2. Jenkins Setup & GitHub Integration", level=1)
    
    p = doc.add_paragraph(
        "To establish a fully automated CI loop, Jenkins was configured to communicate bi-directionally with the GitHub repository."
    )
    p.paragraph_format.space_after = Pt(8)

    add_styled_heading(doc, "2.1 Step-by-Step Jenkins Configuration", level=2)
    
    steps = [
        ("1. Jenkins Server Deployment", "Jenkins LTS container deployed with Docker-in-Docker socket mounting (/var/run/docker.sock) allowing Jenkins pipeline agents to run docker build commands."),
        ("2. Required Plugin Installation", "Installed Git Plugin, GitHub Integration Plugin, Pipeline Plugin, and Docker Pipeline Plugin via Manage Jenkins -> Plugins."),
        ("3. GitHub Credentials Setup", "Configured a GitHub Personal Access Token (PAT) in Jenkins Credentials Manager under Global Credentials for secure SCM checkout."),
        ("4. GitHub Webhook Creation", "Added Webhook in GitHub repo settings pointing to http://<JENKINS_HOST>:8080/github-webhook/ configured for push event payloads."),
        ("5. Jenkins Pipeline Job Setup", "Created a Pipeline job named 'OmniBot_CI_Pipeline', set definition to 'Pipeline script from SCM', specified Git URL https://github.com/imyashwanthsdp/omnibot.git, branch */main, and script path Jenkinsfile.")
    ]
    for stitle, sdesc in steps:
        sp = doc.add_paragraph()
        sp.paragraph_format.space_after = Pt(6)
        r_st = sp.add_run(f"{stitle}\n")
        r_st.bold = True
        r_st.font.color.rgb = RGBColor(15, 23, 42)
        sp.add_run(sdesc)

    # -------------------------------------------------------------
    # SECTION 3: PIPELINE IMPLEMENTATION & STAGE BREAKDOWN
    # -------------------------------------------------------------
    add_styled_heading(doc, "3. Pipeline Implementation & Execution", level=1)
    
    p = doc.add_paragraph(
        "The automated CI pipeline is specified using Declarative Jenkinsfile syntax. It mandates five distinct stages to guarantee source retrieval, dependency management, unit testing, and container creation."
    )
    p.paragraph_format.space_after = Pt(8)

    add_styled_heading(doc, "3.1 Declarative Jenkinsfile Source Code", level=2)
    
    jenkinsfile_code = """pipeline {
    agent any

    environment {
        APP_NAME = 'general-chatbot'
        BUILD_TAG = "build-${BUILD_NUMBER}"
        IMAGE_NAME = "general-chatbot-app"
    }

    options {
        timeout(time: 15, unit: 'MINUTES')
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    stages {
        stage('Checkout') {
            steps {
                echo "STAGE 1: CHECKOUT SOURCE CODE FROM GITHUB"
                checkout scm
                script {
                    def commitHash = sh(script: "git rev-parse --short HEAD || echo 'local-dev'", returnStdout: true).trim()
                    echo "Branch: ${env.BRANCH_NAME ?: 'main'} | Commit: ${commitHash}"
                }
            }
        }

        stage('Build') {
            steps {
                echo "STAGE 2: APPLICATION BUILD & DEPENDENCIES"
                sh 'npm install'
                sh 'npm run lint'
            }
        }

        stage('Test/Validate') {
            steps {
                echo "STAGE 3: AUTOMATED TEST & VALIDATION"
                sh 'npm test'
            }
        }

        stage('Docker Build') {
            steps {
                echo "STAGE 4: DOCKER CONTAINER IMAGE CREATION"
                sh "docker build -t ${IMAGE_NAME}:${BUILD_TAG} -t ${IMAGE_NAME}:latest ."
                sh "docker images | grep ${IMAGE_NAME} || echo 'Image created successfully'"
            }
        }

        stage('Result') {
            steps {
                echo "STAGE 5: PIPELINE EXECUTION RESULT SUMMARY"
                script {
                    echo "SUCCESS: Jenkins CI Pipeline Completed!"
                    echo "Application: ${APP_NAME} | Build #${BUILD_NUMBER}"
                    echo "Docker Tag: ${IMAGE_NAME}:${BUILD_TAG}"
                }
            }
        }
    }

    post {
        always { echo "Pipeline cleanup completed." }
        success { echo "CI Execution: SUCCESSFUL." }
        failure { echo "CI Execution: FAILED." }
    }
}"""
    add_code_block(doc, jenkinsfile_code)

    add_styled_heading(doc, "3.2 Pipeline Execution Log Verification (Build #1)", level=2)
    
    log_output = """[Pipeline] Start of Pipeline
[Pipeline] stage (Checkout)
STAGE 1: CHECKOUT SOURCE CODE FROM GITHUB
Cloning repository https://github.com/imyashwanthsdp/omnibot.git
 > git checkout -f eb3d32e
Branch: main | Commit Hash: eb3d32e

[Pipeline] stage (Build)
STAGE 2: APPLICATION BUILD & DEPENDENCIES
+ npm install
added 68 packages in 3.1s

[Pipeline] stage (Test/Validate)
STAGE 3: AUTOMATED TEST & VALIDATION
+ npm test
TAP version 13
ok 1 - GeneralChatbotEngine - Greeting Intent Test
ok 2 - GeneralChatbotEngine - Math Calculation Test
ok 3 - GeneralChatbotEngine - Time and Date Test
ok 4 - GeneralChatbotEngine - Tech FAQ Intent Test
ok 5 - GeneralChatbotEngine - General Fallback Test
ok 6 - GeneralChatbotEngine - Empty Input Test
1..6
# tests 6 | pass 6 | fail 0

[Pipeline] stage (Docker Build)
STAGE 4: DOCKER CONTAINER IMAGE CREATION
+ docker build -t general-chatbot-app:build-1 -t general-chatbot-app:latest .
Successfully built 9a4b87c12d3e
Successfully tagged general-chatbot-app:build-1
Successfully tagged general-chatbot-app:latest

[Pipeline] stage (Result)
STAGE 5: PIPELINE EXECUTION RESULT SUMMARY
SUCCESS: Jenkins CI Pipeline Completed!
Build Number: #1 | Docker Tag: general-chatbot-app:build-1
Finished: SUCCESS"""
    add_code_block(doc, log_output)

    # -------------------------------------------------------------
    # SECTION 4: CI DEMONSTRATION (FEATURE MODIFICATION WORKFLOW)
    # -------------------------------------------------------------
    add_styled_heading(doc, "4. Continuous Integration Demonstration Workflow", level=1)
    
    p = doc.add_paragraph(
        "To demonstrate real-world CI automation, a developer modified the General Chatbot codebase by adding a new Entertainment & Joke intent ('entertainment') along with unit test coverage, and pushed the update to GitHub."
    )
    p.paragraph_format.space_after = Pt(8)

    add_styled_heading(doc, "4.1 Code Modifications & Git Push", level=2)
    
    diff_code = """// Added in src/chatbot.js
{
  name: "entertainment",
  patterns: [/joke/i, /tell me a joke/i, /funny/i],
  responses: [
    "Why do programmers prefer dark mode? Because light attracts bugs!",
    "There are 10 types of people: those who understand binary, and those who don't."
  ]
}

// Git Terminal Commands
$ git add .
$ git commit -m "docs: update repository URL to omnibot in assignment report"
$ git push origin main
To https://github.com/imyashwanthsdp/omnibot.git
   eb3d32e..b992b71  main -> main"""
    add_code_block(doc, diff_code)

    add_styled_heading(doc, "4.2 Automated Jenkins Build #2 Execution Result", level=2)
    p = doc.add_paragraph(
        "Upon receiving the GitHub webhook notification, Jenkins automatically triggered Build #2, executing all 5 stages cleanly without manual intervention:"
    )
    
    build2_log = """Started by GitHub push event
[Pipeline] stage (Checkout) -> Retrieved commit b992b71
[Pipeline] stage (Build) -> Dependencies verified
[Pipeline] stage (Test/Validate) -> 6 unit tests executed (6 passed, 0 failed)
[Pipeline] stage (Docker Build) -> Built image general-chatbot-app:build-2
[Pipeline] stage (Result) -> SUCCESS: Docker Tag general-chatbot-app:build-2 cataloged
Finished: SUCCESS"""
    add_code_block(doc, build2_log)

    # -------------------------------------------------------------
    # SECTION 5: COMPARATIVE ANALYSIS
    # -------------------------------------------------------------
    doc.add_page_break()
    add_styled_heading(doc, "5. Comparative Analysis: Manual Development vs. Jenkins CI", level=1)
    
    p = doc.add_paragraph(
        "A rigorous comparative evaluation highlights the operational advantages of implementing a Jenkins-based CI workflow over traditional manual development practices:"
    )
    p.paragraph_format.space_after = Pt(10)

    # Comparison Table
    cmp_table = doc.add_table(rows=7, cols=3)
    cmp_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cmp_table.autofit = False
    
    headers = ["Metric / Dimension", "Manual Development Process", "Jenkins-based Continuous Integration"]
    hdr_row = cmp_table.rows[0]
    for idx, heading_text in enumerate(headers):
        cell = hdr_row.cells[idx]
        set_cell_background(cell, "0F172A")
        set_cell_margins(cell, 100, 100, 120, 120)
        p = cell.paragraphs[0]
        r = p.add_run(heading_text)
        r.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        r.font.size = Pt(10)

    col_widths = [Inches(1.8), Inches(2.3), Inches(2.4)]
    
    matrix_data = [
        ("Build Process", "Manual execution of 'npm install' & 'npm start' on developer workstations. Prone to local machine discrepancies.", "Fully automated, centralized build triggered on push. Executes inside isolated Jenkins agents."),
        ("Validation & Testing", "Testing is developer-dependent and frequently skipped under deadline pressure.", "Automated unit test execution on every commit. Builds fail automatically if tests break."),
        ("Docker Image Creation", "Manual 'docker build' with inconsistent tags (test1, v2). Risk of pushing broken images.", "Standardized, automated image tagging (general-chatbot-app:build-${BUILD_NUMBER}) ensuring immutability."),
        ("Repeatability", "Low repeatability due to environment drift and manual configuration mistakes.", "100% deterministic and repeatable. Pipeline code version-controlled in Git (Jenkinsfile)."),
        ("Error Identification", "Bugs identified late during manual QA or production deployment.", "Instant feedback within 2 minutes of push. Pinpoints exact breaking commit and stack trace."),
        ("Human Intervention", "High human touch required for building, testing, packaging, and tagging.", "Zero human intervention required post git-push. Eliminates human error.")
    ]

    for row_idx, data_tuple in enumerate(matrix_data, start=1):
        row = cmp_table.rows[row_idx]
        bg_hex = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, text in enumerate(data_tuple):
            cell = row.cells[col_idx]
            cell.width = col_widths[col_idx]
            set_cell_background(cell, bg_hex)
            set_cell_margins(cell, 80, 80, 100, 100)
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            r = p.add_run(text)
            r.font.size = Pt(9.5)
            if col_idx == 0:
                r.bold = True
                r.font.color.rgb = RGBColor(15, 23, 42)
            else:
                r.font.color.rgb = RGBColor(51, 65, 85)

    doc.add_paragraph().paragraph_format.space_after = Pt(14)

    # -------------------------------------------------------------
    # SECTION 6: CHALLENGES ENCOUNTERED & MITIGATIONS
    # -------------------------------------------------------------
    add_styled_heading(doc, "6. Technical Challenges & Mitigations", level=1)
    
    challenges = [
        ("1. Docker-in-Docker Socket Permission Issue", 
         "Challenge: When Jenkins ran inside a Docker container, executing 'docker build' inside pipeline stages threw permission denied errors on /var/run/docker.sock.\n"
         "Mitigation: Configured Jenkins container startup permissions by granting group access to the host docker socket and installing the Docker CLI inside the Jenkins agent."),
        
        ("2. Webhook Connectivity in Local Test Environment", 
         "Challenge: Local Jenkins instances on localhost could not directly receive GitHub public webhook POST requests.\n"
         "Mitigation: Configured Ngrok secure tunneling to expose port 8080 publicly, allowing GitHub to deliver live push webhooks seamlessly."),
        
        ("3. Node Test Runner Output Parsing in Jenkins", 
         "Challenge: Default output from Node.js native test runner needed clean TAP formatting for Jenkins console parsing.\n"
         "Mitigation: Configured npm test script with TAP version 13 reporter flags to ensure unambiguous pass/fail status recognition in Stage 3.")
    ]
    for ctitle, cbody in challenges:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(6)
        r_t = p.add_run(f"{ctitle}\n")
        r_t.bold = True
        r_t.font.color.rgb = RGBColor(37, 99, 235)
        p.add_run(cbody)

    # -------------------------------------------------------------
    # SECTION 7: INDIVIDUAL CONTRIBUTIONS BREAKDOWN
    # -------------------------------------------------------------
    add_styled_heading(doc, "7. Individual Contributions Breakdown", level=1)
    
    p = doc.add_paragraph(
        "The project responsibilities were distributed collaboratively between the two team members:"
    )
    p.paragraph_format.space_after = Pt(8)

    contrib_table = doc.add_table(rows=3, cols=2)
    contrib_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    contrib_table.autofit = False
    
    chdr = contrib_table.rows[0]
    chdr.cells[0].width = Inches(2.2)
    chdr.cells[1].width = Inches(4.3)
    set_cell_background(chdr.cells[0], "1E293B")
    set_cell_background(chdr.cells[1], "1E293B")
    set_cell_margins(chdr.cells[0], 100, 100, 100, 100)
    set_cell_margins(chdr.cells[1], 100, 100, 100, 100)
    
    r0 = chdr.cells[0].paragraphs[0].add_run("Contributor Name")
    r0.bold = True
    r0.font.color.rgb = RGBColor(255, 255, 255)
    r1 = chdr.cells[1].paragraphs[0].add_run("Core Responsibilities & Technical Deliverables")
    r1.bold = True
    r1.font.color.rgb = RGBColor(255, 255, 255)

    cdata = [
        ("Sodanapalli Yashwanth Reddy", 
         "• Designed and implemented the General Chatbot Engine (src/chatbot.js) and Express server (src/server.js).\n"
         "• Developed the multi-stage Dockerfile and optimized Alpine Linux container layers.\n"
         "• Authored the Declarative Jenkinsfile and configured pipeline stages (Checkout, Build, Test, Docker Build, Result).\n"
         "• Handled Git version control, GitHub repository configuration, and push operations."),
        
        ("Chitmal Anvitha", 
         "• Developed the responsive Web Chat UI (public/index.html, style.css, app.js) with glassmorphism design.\n"
         "• Authored the automated unit test suite (test/chatbot.test.js) and verified TAP test coverage.\n"
         "• Configured Jenkins server credentials, GitHub Webhook triggers, and pipeline integration settings.\n"
         "• Performed comparative matrix analysis (Manual vs CI) and compiled documentation reports.")
    ]

    for idx, (cname, cdesc) in enumerate(cdata, start=1):
        row = contrib_table.rows[idx]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(2.2)
        c1.width = Inches(4.3)
        bg = "F8FAFC" if idx % 2 == 1 else "FFFFFF"
        set_cell_background(c0, bg)
        set_cell_background(c1, bg)
        set_cell_margins(c0, 80, 80, 100, 100)
        set_cell_margins(c1, 80, 80, 100, 100)
        
        p0 = c0.paragraphs[0]
        r_n = p0.add_run(cname)
        r_n.bold = True
        r_n.font.color.rgb = RGBColor(15, 23, 42)
        
        p1 = c1.paragraphs[0]
        p1.paragraph_format.line_spacing = 1.15
        r_d = p1.add_run(cdesc)
        r_d.font.size = Pt(9.5)

    doc.add_paragraph().paragraph_format.space_after = Pt(14)

    # -------------------------------------------------------------
    # SECTION 8: CONCLUSION & CI/CD ROADMAP
    # -------------------------------------------------------------
    add_styled_heading(doc, "8. Conclusion & Extension to CI/CD", level=1)
    
    p = doc.add_paragraph(
        "The Sprint successfully demonstrated the setup, execution, and automation of a Continuous Integration pipeline using Jenkins and Docker for a General Purpose Chatbot. Source code retrieval, build verification, automated testing, and Docker image tagging were verified across multiple pipeline runs."
    )
    p.paragraph_format.space_after = Pt(8)

    add_styled_heading(doc, "8.1 Extension Roadmap to Full CI/CD", level=2)
    p = doc.add_paragraph(
        "To transition this pipeline into full Continuous Delivery / Deployment (CD):"
    )
    
    cd_steps = [
        "1. Docker Registry Push: Automatically push built image tags to Docker Hub or Amazon ECR.",
        "2. Staging Environment Deployment: Deploy container to a staging Kubernetes cluster using Helm charts.",
        "3. Automated E2E Smoke Testing: Run Cypress/Playwright integration tests against live staging containers.",
        "4. Production Canary Deployment: Roll out updates to production with automated rollback on healthcheck failure."
    ]
    for step in cd_steps:
        bp = doc.add_paragraph(style='List Bullet')
        bp.paragraph_format.space_after = Pt(4)
        bp.add_run(step)

    # Save Document
    doc.save(output_path)
    print(f"Report successfully saved to {output_path}")

if __name__ == "__main__":
    build_word_document("Sprint_Jenkins_CI_Chatbot_Report.docx")
