import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_sprint_presentation(output_path):
    prs = Presentation()
    # 16:9 Widescreen Layout
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    blank_layout = prs.slide_layouts[6]

    # Color Palette
    DARK_SLATE = RGBColor(15, 23, 42)    # #0f172a
    ROYAL_BLUE = RGBColor(37, 99, 235)   # #2563eb
    LIGHT_BG   = RGBColor(248, 250, 252) # #f8fafc
    TEXT_DARK  = RGBColor(30, 41, 59)    # #1e293b
    TEXT_MUTED = RGBColor(100, 116, 139) # #64748b
    GREEN_ACCENT = RGBColor(16, 185, 129)# #10b981
    WHITE      = RGBColor(255, 255, 255)

    def add_header(slide, title_text, category_text="SPRINT REVIEW"):
        # Header background banner
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.1))
        tf = header_box.text_frame
        tf.word_wrap = True
        
        p_cat = tf.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = ROYAL_BLUE
        
        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = DARK_SLATE

    # =========================================================================
    # SLIDE 1: Title / Cover Slide
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = DARK_SLATE
    bg1.line.fill.background()

    # Title Box
    tbox1 = slide1.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.333), Inches(4.0))
    tf1 = tbox1.text_frame
    tf1.word_wrap = True

    p1 = tf1.paragraphs[0]
    p1.text = "SPRINT REVIEW PRESENTATION"
    p1.font.size = Pt(13)
    p1.font.bold = True
    p1.font.color.rgb = ROYAL_BLUE

    p2 = tf1.add_paragraph()
    p2.text = "Continuous Integration Pipeline using Jenkins & Docker"
    p2.font.size = Pt(32)
    p2.font.bold = True
    p2.font.color.rgb = WHITE

    p3 = tf1.add_paragraph()
    p3.text = "General Purpose AI Chatbot Application (OmniBot)"
    p3.font.size = Pt(20)
    p3.font.color.rgb = GREEN_ACCENT

    p4 = tf1.add_paragraph()
    p4.text = "\nContributors: Sodanapalli Yashwanth Reddy  |  Chitmal Anvitha\nGitHub Repo: https://github.com/imyashwanthsdp/omnibot"
    p4.font.size = Pt(13)
    p4.font.color.rgb = RGBColor(203, 213, 225)

    # =========================================================================
    # SLIDE 2: Sprint Goals & User Stories
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    add_header(slide2, "Sprint Objectives & Key User Stories")

    goals = [
        ("Goal 1: Jenkins SCM Integration", "Set up Jenkins server and connect it to GitHub via secure webhooks for automatic push detection."),
        ("Goal 2: Pipeline Automation", "Create a root Jenkinsfile defining 5 stages: Checkout -> Build -> Test/Validate -> Docker Build -> Result."),
        ("Goal 3: Automated Testing & Gates", "Execute automated TAP unit tests on every commit; enforce build failure if test assertions break."),
        ("Goal 4: Containerization & Tagging", "Build Docker images automatically and assign immutable tags (general-chatbot-app:build-${BUILD_NUMBER})."),
        ("Goal 5: CI Demonstration", "Push a live feature iteration (entertainment intent) and demonstrate end-to-end headless pipeline execution.")
    ]

    y_pos = Inches(1.8)
    for title, desc in goals:
        box = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), y_pos, Inches(11.733), Inches(0.9))
        box.fill.solid()
        box.fill.fore_color.rgb = LIGHT_BG
        box.line.color.rgb = RGBColor(226, 232, 240)
        
        tf = box.text_frame
        tf.word_wrap = True
        p_t = tf.paragraphs[0]
        p_t.text = title
        p_t.font.size = Pt(14)
        p_t.font.bold = True
        p_t.font.color.rgb = ROYAL_BLUE
        
        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(11)
        p_d.font.color.rgb = TEXT_DARK
        
        y_pos += Inches(1.05)

    # =========================================================================
    # SLIDE 3: Application & Architecture Overview
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    add_header(slide3, "OmniBot Architecture & Application Stack")

    # Text Card (Left)
    l_box = slide3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.5), Inches(5.0))
    l_box.fill.solid()
    l_box.fill.fore_color.rgb = LIGHT_BG
    l_box.line.color.rgb = RGBColor(226, 232, 240)
    
    tf = l_box.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = "Key Application Modules:"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = DARK_SLATE

    items = [
        "src/chatbot.js: General Chatbot Engine (Greetings, Math, Time/Date, Tech FAQs, Fallback).",
        "src/server.js: Express Server exposing REST API (/api/chat & /api/health).",
        "public/: Responsive Glassmorphism UI with dark mode & action chips.",
        "test/chatbot.test.js: Automated TAP unit test suite (6/6 tests passing).",
        "Dockerfile: Alpine-based multi-stage container specification.",
        "Jenkinsfile: Pipeline as Code defining automated CI workflow."
    ]
    for item in items:
        p_i = tf.add_paragraph()
        p_i.text = f"• {item}"
        p_i.font.size = Pt(11)
        p_i.font.color.rgb = TEXT_DARK

    # Screenshot Image (Right)
    img1_path = os.path.join("screenshots", "screenshot1_chatbot_ui.png")
    if os.path.exists(img1_path):
        slide3.shapes.add_picture(img1_path, Inches(6.6), Inches(1.8), width=Inches(5.9))

    # =========================================================================
    # SLIDE 4: Jenkins Pipeline Implementation
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    add_header(slide4, "Jenkins Pipeline Implementation (5 Stages)")

    # Pipeline Diagram Box (Top)
    img5_path = os.path.join("screenshots", "screenshot5_jenkins_stageview.png")
    if os.path.exists(img5_path):
        slide4.shapes.add_picture(img5_path, Inches(0.8), Inches(1.7), width=Inches(11.733))

    # Stage Explanations (Bottom Grid)
    stages_info = [
        ("1. Checkout", "Clones git commit from origin repository."),
        ("2. Build", "Installs npm dependencies & runs lint check."),
        ("3. Test/Validate", "Executes 6 unit tests with TAP output."),
        ("4. Docker Build", "Builds image tagged general-chatbot-app:build-N."),
        ("5. Result", "Summarizes pipeline telemetry & verifies image tag.")
    ]

    x_pos = Inches(0.8)
    for s_name, s_desc in stages_info:
        s_box = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x_pos, Inches(5.1), Inches(2.15), Inches(1.8))
        s_box.fill.solid()
        s_box.fill.fore_color.rgb = LIGHT_BG
        s_box.line.color.rgb = ROYAL_BLUE
        
        tf = s_box.text_frame
        tf.word_wrap = True
        p_h = tf.paragraphs[0]
        p_h.text = s_name
        p_h.font.size = Pt(12)
        p_h.font.bold = True
        p_h.font.color.rgb = ROYAL_BLUE
        
        p_b = tf.add_paragraph()
        p_b.text = s_desc
        p_b.font.size = Pt(10)
        p_b.font.color.rgb = TEXT_DARK
        
        x_pos += Inches(2.4)

    # =========================================================================
    # SLIDE 5: Automated CI Demonstration Workflow
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    add_header(slide5, "Continuous Integration Demonstration & Verification")

    # Left Text
    l_box = slide5.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.5), Inches(5.0))
    l_box.fill.solid()
    l_box.fill.fore_color.rgb = LIGHT_BG
    l_box.line.color.rgb = RGBColor(226, 232, 240)
    
    tf = l_box.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = "Feature Modification & Push Workflow:"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = DARK_SLATE

    demo_steps = [
        "Code Update: Added 'entertainment' intent (jokes) to chatbot engine.",
        "Git Commit & Push: Committed changes and pushed to GitHub main branch.",
        "Automated Webhook: GitHub notified Jenkins via POST webhook payload.",
        "Pipeline Execution (Build #2): Jenkins automatically triggered Build #2.",
        "Validation Outcome: 6/6 tests passed, created Docker tag general-chatbot-app:build-2."
    ]
    for step in demo_steps:
        p_s = tf.add_paragraph()
        p_s.text = f"✔ {step}"
        p_s.font.size = Pt(11)
        p_s.font.color.rgb = TEXT_DARK

    # Right Image: Git Commits
    img6_path = os.path.join("screenshots", "screenshot6_github_commits.png")
    if os.path.exists(img6_path):
        slide5.shapes.add_picture(img6_path, Inches(6.6), Inches(1.8), width=Inches(5.9))

    # =========================================================================
    # SLIDE 6: Comparative Analysis (Manual vs Jenkins CI)
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    add_header(slide6, "Comparative Analysis: Manual vs. Jenkins CI")

    cards = [
        ("Build & Dependencies", "Manual npm install on local machines prone to environment drift.", "Automated, centralized build triggered on push in clean Jenkins agent."),
        ("Validation & Testing", "Developer-dependent; tests frequently skipped under tight deadlines.", "Automated TAP test execution on every commit; blocks broken builds."),
        ("Docker Container Tagging", "Inconsistent manual tags (test1, v2). Risk of broken deployments.", "Immutable automated tags (general-chatbot-app:build-${BUILD_NUMBER})."),
        ("Error Identification", "Defects caught late during manual QA or production deployment.", "Instant feedback within 2 minutes of push with exact failure context."),
        ("Human Intervention", "High manual touch required for building, testing, packaging, tagging.", "Zero human intervention post git-push. Completely automated.")
    ]

    y_p = Inches(1.7)
    for metric, manual_text, ci_text in cards:
        c_box = slide6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), y_p, Inches(11.733), Inches(0.95))
        c_box.fill.solid()
        c_box.fill.fore_color.rgb = LIGHT_BG
        c_box.line.color.rgb = RGBColor(226, 232, 240)
        
        tf = c_box.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = f"Metric: {metric}"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = ROYAL_BLUE
        
        p_m = tf.add_paragraph()
        p_m.text = f"Manual: {manual_text}  |  Jenkins CI: {ci_text}"
        p_m.font.size = Pt(10.5)
        p_m.font.color.rgb = TEXT_DARK
        
        y_p += Inches(1.05)

    # =========================================================================
    # SLIDE 7: Team Contributions & CI/CD Extension Roadmap
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    add_header(slide7, "Team Contributions & CI/CD Roadmap")

    # Left Box: Team Contributions
    t1_box = slide7.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0))
    t1_box.fill.solid()
    t1_box.fill.fore_color.rgb = LIGHT_BG
    t1_box.line.color.rgb = RGBColor(226, 232, 240)
    tf1 = t1_box.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "Individual Contribution Split:"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = DARK_SLATE

    p_y = tf1.add_paragraph()
    p_y.text = "Sodanapalli Yashwanth Reddy:"
    p_y.font.size = Pt(12)
    p_y.font.bold = True
    p_y.font.color.rgb = ROYAL_BLUE
    
    p_yd = tf1.add_paragraph()
    p_yd.text = "• Chatbot Engine & Express API Server\n• Multi-stage Dockerfile & Alpine optimization\n• Declarative Jenkinsfile & SCM Pipeline\n• Git version control & GitHub push operations"
    p_yd.font.size = Pt(10)
    p_yd.font.color.rgb = TEXT_DARK

    p_a = tf1.add_paragraph()
    p_a.text = "\nChitmal Anvitha:"
    p_a.font.size = Pt(12)
    p_a.font.bold = True
    p_a.font.color.rgb = ROYAL_BLUE
    
    p_ad = tf1.add_paragraph()
    p_ad.text = "• Web Chat UI (HTML/CSS/JS) with Glassmorphism\n• Automated TAP unit test suite (6/6 passing)\n• Jenkins server credentials & GitHub Webhooks\n• Comparative matrix analysis & documentation"
    p_ad.font.size = Pt(10)
    p_ad.font.color.rgb = TEXT_DARK

    # Right Box: Extension to CI/CD
    t2_box = slide7.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0))
    t2_box.fill.solid()
    t2_box.fill.fore_color.rgb = LIGHT_BG
    t2_box.line.color.rgb = RGBColor(226, 232, 240)
    tf2 = t2_box.text_frame
    tf2.word_wrap = True

    p = tf2.paragraphs[0]
    p.text = "Roadmap to Full CI/CD Extension:"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = DARK_SLATE

    roadmap_steps = [
        "1. Docker Registry Push: Push built images to Docker Hub or Amazon ECR.",
        "2. Staging Deployment: Deploy container to staging Kubernetes cluster using Helm.",
        "3. Automated E2E Smoke Testing: Run Cypress/Playwright integration tests against staging.",
        "4. Production Canary Release: Zero-downtime production deployment with automated rollback on failure."
    ]
    for rstep in roadmap_steps:
        p_r = tf2.add_paragraph()
        p_r.text = f"\n🚀 {rstep}"
        p_r.font.size = Pt(10.5)
        p_r.font.color.rgb = TEXT_DARK

    prs.save(output_path)
    print(f"Presentation successfully saved to {output_path}")

if __name__ == "__main__":
    create_sprint_presentation("Sprint_Review_OmniBot_CI.pptx")
