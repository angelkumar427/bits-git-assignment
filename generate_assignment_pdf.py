import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        print(f"Total PDF Pages: {num_pages}")
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#4A5568"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 755, "ASSIGNMENT 1: GIT WORKFLOW & TEST CASE DESIGN")
            self.drawRightString(558, 755, "STUDENT: Angel Kumar (2024eb02187)")
            self.setStrokeColor(colors.HexColor("#CBD5E0"))
            self.setLineWidth(0.75)
            self.line(54, 747, 558, 747)

        # Footer (all pages)
        self.setStrokeColor(colors.HexColor("#CBD5E0"))
        self.setLineWidth(0.75)
        self.line(54, 45, 558, 45)
        
        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor("#718096"))
        self.drawString(54, 32, "Academic Submission | BITS Pilani | Total Marks: 20 | Single Deliverable PDF")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 32, page_str)
        self.restoreState()

def build_pdf(filename="BITS_Assignment_Solutions.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    primary_color = colors.HexColor("#1A365D")    # Deep Navy
    secondary_color = colors.HexColor("#2B6CB0")  # Slate Blue
    accent_color = colors.HexColor("#2C7A7B")     # Dark Teal
    text_dark = colors.HexColor("#2D3748")        # Charcoal Text
    bg_light = colors.HexColor("#F7FAFC")         # Off-white
    code_bg = colors.HexColor("#1A202C")          # Dark Console BG

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=primary_color,
        spaceAfter=3
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=secondary_color,
        spaceAfter=10
    )

    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12.5,
        leading=16,
        textColor=primary_color,
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=secondary_color,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=text_dark,
        spaceAfter=5
    )

    meta_label = ParagraphStyle(
        'MetaLabel',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=primary_color
    )

    meta_val = ParagraphStyle(
        'MetaVal',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=text_dark
    )

    terminal_style = ParagraphStyle(
        'Terminal',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7,
        leading=9.5,
        textColor=colors.HexColor("#E2E8F0")
    )

    tbl_header = ParagraphStyle(
        'TblHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.white
    )

    tbl_body = ParagraphStyle(
        'TblBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.2,
        leading=9.5,
        textColor=text_dark
    )

    tbl_body_bold = ParagraphStyle(
        'TblBodyBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.2,
        leading=9.5,
        textColor=primary_color
    )

    tbl_code = ParagraphStyle(
        'TblCode',
        parent=styles['Normal'],
        fontName='Courier-Bold',
        fontSize=7,
        leading=9,
        textColor=colors.HexColor("#6B46C1")
    )

    story = []

    # ==========================================
    # PAGE 1: TITLE, META, QUESTION 1 (STEP 1 & 2)
    # ==========================================
    story.append(Paragraph("BITS PILANI - WORK INTEGRATED LEARNING PROGRAMMES", subtitle_style))
    story.append(Paragraph("COURSE ASSIGNMENT 1: SOLUTIONS DOCUMENT", title_style))
    story.append(Paragraph("Covers: Question 1 (Git &amp; GitHub Workflow) &amp; Question 2 (Test Case Design)", subtitle_style))
    
    meta_data = [
        [
            Paragraph("<b>Course:</b> Software Engineering &amp; DevOps", meta_label),
            Paragraph("<b>Total Score:</b> 20 Marks (10% of Final Module Grade)", meta_label)
        ],
        [
            Paragraph("<b>Student Name:</b> Angel Kumar", meta_val),
            Paragraph("<b>Roll No:</b> 2024eb02187", meta_val)
        ],
        [
            Paragraph("<b>Email:</b> 2024eb02187@online.bits-pilani.ac.in", meta_val),
            Paragraph("<b>GitHub URL:</b> https://github.com/angelkumar427/bits-git-assignment", meta_val)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[250, 254])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F0F4F8")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E0")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 6))

    story.append(Paragraph("QUESTION 1: Git &amp; GitHub Workflow (10 Marks)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=6))
    
    q1_summary = (
        "<b>Workflow Overview:</b> This task demonstrates end-to-end local version control operations, "
        "including repository initialization, multi-commit history, branch creation, isolated feature development, "
        "non-fast-forward branch integration, file exclusion with <code>.gitignore</code>, and safe undo operations. "
        "The repository was created locally first, and finally pushed to a public GitHub repository."
    )
    story.append(Paragraph(q1_summary, body_style))

    story.append(Paragraph("Step 1: Local Repository Setup (2 Marks)", h2_style))
    s1_text = (
        "A local project directory was initialized without creating the remote repository first. Two essential HTML "
        "files (<code>index.html</code> and <code>about.html</code>) were authored with clean semantic structure. "
        "The default branch was configured to <code>main</code>."
    )
    story.append(Paragraph(s1_text, body_style))

    c1 = (
        "$ mkdir bits &amp;&amp; cd bits<br/>"
        "$ git init<br/>"
        "Initialized empty Git repository in C:/Users/kumar/OneDrive/Documents/bits/.git/<br/>"
        "$ git branch -M main<br/>"
        "$ git status<br/>"
        "On branch main | No commits yet | Untracked files: about.html, index.html"
    )
    t1 = Table([[Paragraph(c1, terminal_style)]], colWidths=[504])
    t1.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), code_bg), ('PADDING', (0, 0), (-1, -1), 5)]))
    story.append(t1)
    story.append(Spacer(1, 4))

    story.append(Paragraph("Step 2: Git Workflow Execution - Commits, Branching &amp; Merging (4 Marks)", h2_style))
    s2_text = (
        "<b>Executed Sequence:</b><br/>"
        "1. <b>Initial Commit:</b> Staged and committed <code>index.html</code> and <code>about.html</code> (commit <code>eca2d40</code>).<br/>"
        "2. <b>Second Commit:</b> Modified <code>about.html</code> adding project objectives and committed (commit <code>a08561d</code>).<br/>"
        "3. <b>Branching:</b> Created and switched to <code>feature</code> branch using <code>git checkout -b feature</code>.<br/>"
        "4. <b>Feature Commit:</b> Added feature cards in <code>index.html</code> and committed on <code>feature</code> (commit <code>ff55e28</code>).<br/>"
        "5. <b>Integration &amp; Log Graph:</b> Switched to <code>main</code> and merged <code>feature</code> using <code>--no-ff</code> to create merge commit <code>24e7a45</code>, preserving branch history."
    )
    story.append(Paragraph(s2_text, body_style))

    c2 = (
        "$ git commit -m \"Initial commit: Add index.html and about.html\" -&gt; [main (root) eca2d40]<br/>"
        "$ git commit -m \"Update about.html: Add project objectives and details\" -&gt; [main a08561d]<br/>"
        "$ git branch feature &amp;&amp; git checkout feature &amp;&amp; git commit -m \"Feature: Add key features section\" -&gt; [feature ff55e28]<br/>"
        "$ git checkout main &amp;&amp; git merge feature --no-ff -m \"Merge branch 'feature' into main\"<br/>"
        "Merge made by the 'ort' strategy. [commit 24e7a45]<br/>"
        "$ git log --graph --oneline --all --decorate<br/>"
        "*   24e7a45 (HEAD -&gt; main) Merge branch 'feature' into main<br/>"
        "|\\  <br/>"
        "| * ff55e28 (feature) Feature: Add key features section to index.html<br/>"
        "|/  <br/>"
        "* a08561d Update about.html: Add project objectives and details<br/>"
        "* eca2d40 Initial commit: Add index.html and about.html"
    )
    t2 = Table([[Paragraph(c2, terminal_style)]], colWidths=[504])
    t2.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), code_bg), ('PADDING', (0, 0), (-1, -1), 5)]))
    story.append(t2)

    story.append(PageBreak())

    # ==========================================
    # PAGE 2: STEPS 3, 4, 5 (GITIGNORE, UNDO, GITHUB)
    # ==========================================
    story.append(Paragraph("QUESTION 1 (Continued): Git &amp; GitHub Workflow", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=6))

    story.append(Paragraph("Step 3: .gitignore Implementation (1 Mark)", h2_style))
    s3_text = (
        "A <code>.gitignore</code> file was created in the project root configured to exclude all <code>.log</code> files "
        "and the <code>temp/</code> folder. The configuration was tested with <code>app.log</code> and <code>temp/cache.tmp</code>. "
        "As confirmed below, Git completely ignores these files while tracking <code>.gitignore</code>."
    )
    story.append(Paragraph(s3_text, body_style))

    c3 = (
        "=== .gitignore Content ===<br/>"
        "*.log<br/>"
        "temp/<br/><br/>"
        "=== Verification via git status &amp; git check-ignore ===<br/>"
        "$ git status<br/>"
        "Untracked files: .gitignore (Notice app.log and temp/ are completely hidden)<br/>"
        "$ git check-ignore app.log temp/cache.tmp<br/>"
        "app.log<br/>"
        "temp/cache.tmp<br/>"
        "$ git add .gitignore &amp;&amp; git commit -m \"Configure .gitignore to ignore *.log files and temp/ directory\"<br/>"
        "[main b22a713] 1 file changed, 5 insertions(+)"
    )
    t3 = Table([[Paragraph(c3, terminal_style)]], colWidths=[504])
    t3.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), code_bg), ('PADDING', (0, 0), (-1, -1), 5)]))
    story.append(t3)
    story.append(Spacer(1, 6))

    story.append(Paragraph("Step 4: Undo Operation using Git (1 Mark)", h2_style))
    s4_text = (
        "To demonstrate rolling back an erroneous commit safely, an extra commit (<code>f21c795</code>: adding <code>draft_notes.txt</code>) "
        "was recorded. The undo operation was executed using <code>git reset HEAD~1</code>. This moved HEAD back to <code>b22a713</code> "
        "while leaving the working tree files intact as unstaged changes. The repository state before and after confirms the commit was undone."
    )
    story.append(Paragraph(s4_text, body_style))

    c4 = (
        "$ git add draft_notes.txt &amp;&amp; git commit -m \"Temporary commit: Add draft notes\"<br/>"
        "[main f21c795] Temporary commit: Add draft notes | 1 file changed, 2 insertions(+)<br/><br/>"
        "$ git reset HEAD~1<br/>"
        "Unstaged changes after reset: M draft_notes.txt<br/><br/>"
        "$ git log -2 --oneline<br/>"
        "b22a713 Configure .gitignore to ignore *.log files and temp/ directory<br/>"
        "24e7a45 Merge branch 'feature' into main<br/>"
        "(HEAD restored to b22a713; commit f21c795 removed from branch history without loss of work)"
    )
    t4 = Table([[Paragraph(c4, terminal_style)]], colWidths=[504])
    t4.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), code_bg), ('PADDING', (0, 0), (-1, -1), 5)]))
    story.append(t4)
    story.append(Spacer(1, 6))

    story.append(Paragraph("Step 5: GitHub Integration &amp; Public Repository Verification (1 Mark)", h2_style))
    s5_text = (
        "The local repository was published to GitHub under the public profile <code>angelkumar427</code>. "
        "Both the <code>main</code> branch and the <code>feature</code> branch were pushed to remote origin, allowing evaluators "
        "to inspect all commit nodes and branch topologies directly on GitHub.<br/>"
        "• <b>Public GitHub Repository URL:</b> <font color=\"#2B6CB0\"><b><u>https://github.com/angelkumar427/bits-git-assignment</u></b></font><br/>"
        "• <b>Visibility Status:</b> Public (Verified via GitHub API: <code>isPrivate: false</code>)"
    )
    story.append(Paragraph(s5_text, body_style))

    c5 = (
        "$ gh repo create bits-git-assignment --public --source=. --remote=origin --push<br/>"
        "✓ Created repository angelkumar427/bits-git-assignment on GitHub<br/>"
        "✓ Pushed commits to origin/main<br/>"
        "$ git push origin feature<br/>"
        "To https://github.com/angelkumar427/bits-git-assignment.git<br/>"
        " * [new branch]      feature -&gt; feature<br/>"
        "$ gh repo view angelkumar427/bits-git-assignment --json isPrivate,url<br/>"
        "{\"isPrivate\":false,\"url\":\"https://github.com/angelkumar427/bits-git-assignment\"}"
    )
    t5 = Table([[Paragraph(c5, terminal_style)]], colWidths=[504])
    t5.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), code_bg), ('PADDING', (0, 0), (-1, -1), 5)]))
    story.append(t5)

    story.append(PageBreak())

    # ==========================================
    # PAGE 3: STEP 6 COMMAND DOCUMENTATION
    # ==========================================
    story.append(Paragraph("Step 6: Command Documentation File (git_commands.txt) (1 Mark)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=6))
    
    s6_text = (
        "In compliance with Step 6, a dedicated file named <code>git_commands.txt</code> has been created and committed "
        "in the repository root. The comprehensive table below documents all Git commands utilized throughout this assignment "
        "with concise, accurate 1-2 line explanations of their operational role."
    )
    story.append(Paragraph(s6_text, body_style))

    cmd_data = [
        [Paragraph("Git Command Syntax", tbl_header), Paragraph("Operational Explanation / Purpose", tbl_header)],
        [Paragraph("git init", tbl_code), Paragraph("Initializes a new, empty Git repository inside the local project directory.", tbl_body)],
        [Paragraph("git branch -M main", tbl_code), Paragraph("Renames the default branch to 'main' conforming to modern standard Git conventions.", tbl_body)],
        [Paragraph("git status", tbl_code), Paragraph("Displays working directory and staging area status, indicating tracked, untracked, and modified files.", tbl_body)],
        [Paragraph("git add index.html about.html", tbl_code), Paragraph("Stages the newly created index.html and about.html files to prepare them for the root commit.", tbl_body)],
        [Paragraph("git commit -m \"...\"", tbl_code), Paragraph("Records staged file snapshots permanently into repository history with a clear commit message.", tbl_body)],
        [Paragraph("git add about.html", tbl_code), Paragraph("Stages content modifications made to about.html (adding project objectives and details).", tbl_body)],
        [Paragraph("git branch feature", tbl_code), Paragraph("Creates an isolated branch named 'feature' branching off from the current commit on main.", tbl_body)],
        [Paragraph("git checkout feature", tbl_code), Paragraph("Switches the active working directory and HEAD pointer to the 'feature' branch context.", tbl_body)],
        [Paragraph("git add index.html", tbl_code), Paragraph("Stages enhancements made to index.html exclusively within the feature branch.", tbl_body)],
        [Paragraph("git checkout main", tbl_code), Paragraph("Switches the working branch back to 'main' in preparation for branch integration.", tbl_body)],
        [Paragraph("git merge feature --no-ff -m \"...\"", tbl_code), Paragraph("Performs a non-fast-forward merge, creating an explicit merge commit preserving branch history.", tbl_body)],
        [Paragraph("git log --graph --oneline --all", tbl_code), Paragraph("Renders an ASCII visualization of all branches, commits, and merge nodes across history.", tbl_body)],
        [Paragraph("git check-ignore &lt;files&gt;", tbl_code), Paragraph("Debugs and verifies that specified files match active pattern rules in .gitignore.", tbl_body)],
        [Paragraph("git add .gitignore", tbl_code), Paragraph("Stages the .gitignore configuration file configured to ignore *.log files and temp/.", tbl_body)],
        [Paragraph("git reset HEAD~1", tbl_code), Paragraph("Undoes the latest commit by moving HEAD back by 1, preserving working files as unstaged.", tbl_body)],
        [Paragraph("git remote add origin &lt;URL&gt;", tbl_code), Paragraph("Associates the local Git repository with the remote GitHub repository URL.", tbl_body)],
        [Paragraph("git push -u origin main", tbl_code), Paragraph("Pushes local commits on 'main' to GitHub and establishes upstream tracking.", tbl_body)],
        [Paragraph("git push origin feature", tbl_code), Paragraph("Pushes the 'feature' branch to GitHub so multi-branch activity is fully visible online.", tbl_body)]
    ]
    cmd_summary_table = Table(cmd_data, colWidths=[175, 329])
    cmd_summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), secondary_color),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E0")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, bg_light]),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(cmd_summary_table)

    story.append(PageBreak())

    # ==========================================
    # PAGE 4: QUESTION 2 - METHODOLOGY & TC_01 TO TC_06
    # ==========================================
    story.append(Paragraph("QUESTION 2: Test Case Design (10 Marks)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=6))

    q2_overview = (
        "<b>System Under Test (SUT):</b> Authentication Login System<br/>"
        "<b>Inputs:</b> Username (Text Field), Password (Password Field), Login Button (Action Element).<br/>"
        "<b>Functional Requirements (FR):</b><br/>"
        "• <b>FR1:</b> Username must not be empty.<br/>"
        "• <b>FR2:</b> Password must be at least 6 characters long.<br/>"
        "• <b>FR3:</b> Valid username and password allow a successful login.<br/>"
        "• <b>FR4:</b> Invalid credentials should display an error message.<br/>"
        "• <b>FR5:</b> After 3 consecutive failed login attempts, the account should be locked.<br/><br/>"
        "<b>Design Methodology:</b> Applied <b>Equivalence Partitioning (EP)</b> to classify valid/invalid inputs, "
        "<b>Boundary Value Analysis (BVA)</b> at critical password lengths (0, 1, 5, 6, 7 chars), and "
        "<b>State Transition Testing (STT)</b> for the 3-attempt lockout security counter."
    )
    story.append(Paragraph(q2_overview, body_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph("Step 1: Test Case Specification Table (Part 1: Validation & Boundaries)", h2_style))
    
    tc_part1 = [
        [
            Paragraph("Test ID", tbl_header),
            Paragraph("Test Scenario", tbl_header),
            Paragraph("Input Data", tbl_header),
            Paragraph("Expected Output", tbl_header)
        ],
        [
            Paragraph("TC_01", tbl_body_bold),
            Paragraph("Standard Valid Login: Valid registered credentials meeting length rules (> 6 chars) [FR3]", tbl_body),
            Paragraph("Username: <code>user1</code><br/>Password: <code>pass123</code> (7 chars)<br/>Action: Click Login", tbl_body),
            Paragraph("Login successful. Authentication token generated; user redirected to home dashboard with 'Welcome user1' banner.", tbl_body)
        ],
        [
            Paragraph("TC_02", tbl_body_bold),
            Paragraph("Boundary Condition: Valid login with password length exactly equal to minimum requirement (6 chars) [FR2, FR3]", tbl_body),
            Paragraph("Username: <code>user1</code><br/>Password: <code>Abc@12</code> (6 chars)<br/>Action: Click Login", tbl_body),
            Paragraph("Login successful. Exactly 6 characters accepted; user authenticated and redirected to dashboard.", tbl_body)
        ],
        [
            Paragraph("TC_03", tbl_body_bold),
            Paragraph("Empty Username Validation: Submit login form with blank username field [FR1]", tbl_body),
            Paragraph("Username: <code>\"\"</code> (empty string)<br/>Password: <code>pass123</code><br/>Action: Click Login", tbl_body),
            Paragraph("Login rejected. Inline validation error: 'Username must not be empty. Please enter your username.' Form submission blocked.", tbl_body)
        ],
        [
            Paragraph("TC_04", tbl_body_bold),
            Paragraph("Empty Password Validation: Submit login form with blank password field [FR2]", tbl_body),
            Paragraph("Username: <code>user1</code><br/>Password: <code>\"\"</code> (empty string)<br/>Action: Click Login", tbl_body),
            Paragraph("Login rejected. Inline validation error: 'Password must not be empty. Password must be at least 6 characters long.'", tbl_body)
        ],
        [
            Paragraph("TC_05", tbl_body_bold),
            Paragraph("Edge Case: Both username and password fields submitted empty [FR1, FR2]", tbl_body),
            Paragraph("Username: <code>\"\"</code> (empty)<br/>Password: <code>\"\"</code> (empty)<br/>Action: Click Login", tbl_body),
            Paragraph("Login rejected. Both fields highlighted in red with: 'Username must not be empty' and 'Password cannot be empty'.", tbl_body)
        ],
        [
            Paragraph("TC_06", tbl_body_bold),
            Paragraph("Boundary Value Analysis: Password length strictly below minimum boundary (5 characters) [FR2]", tbl_body),
            Paragraph("Username: <code>user1</code><br/>Password: <code>abcde</code> (5 chars)<br/>Action: Click Login", tbl_body),
            Paragraph("Login rejected. Validation message: 'Password must be at least 6 characters long.' Backend auth call suppressed.", tbl_body)
        ],
        [
            Paragraph("TC_07", tbl_body_bold),
            Paragraph("Edge Case: Minimal single character password submission [FR2]", tbl_body),
            Paragraph("Username: <code>user1</code><br/>Password: <code>a</code> (1 char)<br/>Action: Click Login", tbl_body),
            Paragraph("Login rejected. Validation message: 'Password must be at least 6 characters long.' Field marked invalid.", tbl_body)
        ]
    ]

    t_tc1 = Table(tc_part1, colWidths=[40, 150, 125, 189])
    t_tc1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary_color),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E0")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, bg_light]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_tc1)

    story.append(PageBreak())

    # ==========================================
    # PAGE 5: TEST CASES PART 2, RTM & STATE MACHINE
    # ==========================================
    story.append(Paragraph("QUESTION 2 (Continued): Security Scenarios, RTM &amp; State Logic", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=6))

    story.append(Paragraph("Step 1: Test Case Specification Table (Part 2: Security &amp; Lockout Logic)", h2_style))
    
    tc_part2 = [
        [
            Paragraph("Test ID", tbl_header),
            Paragraph("Test Scenario", tbl_header),
            Paragraph("Input Data", tbl_header),
            Paragraph("Expected Output", tbl_header)
        ],
        [
            Paragraph("TC_08", tbl_body_bold),
            Paragraph("Invalid Credentials: Non-existent username with valid password syntax [FR4]", tbl_body),
            Paragraph("Username: <code>ghostUser99</code><br/>Password: <code>pass1234</code><br/>Action: Click Login", tbl_body),
            Paragraph("Login rejected. Generic error: 'Invalid username or password. Please try again.' (Prevents user enumeration).", tbl_body)
        ],
        [
            Paragraph("TC_09", tbl_body_bold),
            Paragraph("Invalid Credentials: Registered username with incorrect password [FR4]", tbl_body),
            Paragraph("Username: <code>user1</code><br/>Password: <code>wrongPassword</code><br/>Action: Click Login", tbl_body),
            Paragraph("Login rejected. Error: 'Invalid username or password. (Remaining attempts: 2)'. Failed attempt counter = 1.", tbl_body)
        ],
        [
            Paragraph("TC_10", tbl_body_bold),
            Paragraph("Account Lockout: Exactly 3 consecutive failed login attempts on registered account [FR5]", tbl_body),
            Paragraph("Username: <code>user1</code><br/>Attempt 1: <code>wrongP1</code> (Fail 1)<br/>Attempt 2: <code>wrongP2</code> (Fail 2)<br/>Attempt 3: <code>wrongP3</code> (Fail 3)", tbl_body),
            Paragraph("Login rejected on attempt 3. Account status transitions to LOCKED. Security message: 'Account locked due to 3 consecutive failed attempts. Please contact support or reset password.'", tbl_body)
        ],
        [
            Paragraph("TC_11", tbl_body_bold),
            Paragraph("Counter Reset Behavior: Successful login following failed attempts before reaching threshold", tbl_body),
            Paragraph("Username: <code>user1</code><br/>Attempt 1: <code>wrongP1</code> (Fail 1)<br/>Attempt 2: <code>wrongP2</code> (Fail 2)<br/>Attempt 3: <code>pass123</code> (Valid)", tbl_body),
            Paragraph("Attempt 3 successful. User redirected to dashboard. Failed attempt counter reset from 2 back to 0 for subsequent logins.", tbl_body)
        ],
        [
            Paragraph("TC_12", tbl_body_bold),
            Paragraph("Locked Account Enforcement: Attempting login on an already locked account with correct credentials", tbl_body),
            Paragraph("Username: <code>user1</code> (Status: Locked)<br/>Password: <code>pass123</code> (Correct)<br/>Action: Click Login", tbl_body),
            Paragraph("Login rejected immediately without credential evaluation. Security alert: 'Your account is locked. Follow unlock instructions sent to registered email.'", tbl_body)
        ]
    ]

    t_tc2 = Table(tc_part2, colWidths=[40, 150, 125, 189])
    t_tc2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary_color),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E0")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, bg_light]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_tc2)
    story.append(Spacer(1, 6))

    story.append(Paragraph("Requirements Traceability Matrix (RTM)", h2_style))
    rtm_data = [
        [Paragraph("Req ID", tbl_header), Paragraph("Functional Requirement Description", tbl_header), Paragraph("Mapped Test Cases", tbl_header), Paragraph("Coverage Status", tbl_header)],
        [Paragraph("FR1", tbl_body_bold), Paragraph("Username must not be empty", tbl_body), Paragraph("TC_03, TC_05", tbl_code), Paragraph("100% (Valid, Empty, Both Empty)", tbl_body)],
        [Paragraph("FR2", tbl_body_bold), Paragraph("Password must be at least 6 characters long", tbl_body), Paragraph("TC_02, TC_04, TC_06, TC_07", tbl_code), Paragraph("100% (BVA: 0, 1, 5, 6 chars)", tbl_body)],
        [Paragraph("FR3", tbl_body_bold), Paragraph("Valid username and password allow successful login", tbl_body), Paragraph("TC_01, TC_02, TC_11", tbl_code), Paragraph("100% (Standard, Boundary, Reset)", tbl_body)],
        [Paragraph("FR4", tbl_body_bold), Paragraph("Invalid credentials display an error message", tbl_body), Paragraph("TC_08, TC_09", tbl_code), Paragraph("100% (Wrong User, Wrong Pass)", tbl_body)],
        [Paragraph("FR5", tbl_body_bold), Paragraph("After 3 consecutive failed attempts, account is locked", tbl_body), Paragraph("TC_10, TC_11, TC_12", tbl_code), Paragraph("100% (Lockout, Reset, Locked Auth)", tbl_body)]
    ]
    t_rtm = Table(rtm_data, colWidths=[45, 230, 115, 114])
    t_rtm.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), secondary_color),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E0")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, bg_light]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_rtm)
    story.append(Spacer(1, 6))

    story.append(Paragraph("Account Lockout State Machine &amp; Security Logic (FR5)", h2_style))
    state_desc = (
        "The lockout functionality implements a Finite State Machine (FSM) to protect against brute-force attacks:<br/>"
        "• <b>State 0 (Active / Unlocked, 0 Fails):</b> Normal state. Correct credentials grant dashboard access.<br/>"
        "• <b>State 1 (Active / Warning, 1 Fail):</b> 1st failure increments counter to 1; displays 2 attempts remaining.<br/>"
        "• <b>State 2 (Active / Critical, 2 Fails):</b> 2nd failure increments counter to 2; displays 1 attempt remaining. If attempt 3 is valid, system transitions back to State 0 (counter resets).<br/>"
        "• <b>State 3 (Locked, 3 Consecutive Fails):</b> 3rd failure locks the account in the database immediately, invalidates active sessions, and requires administrative unlock or password reset."
    )
    story.append(Paragraph(state_desc, body_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated {filename}")

if __name__ == "__main__":
    build_pdf()
