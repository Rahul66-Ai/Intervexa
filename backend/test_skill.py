from utils.resume_parser import extract_resume_text
from utils.skill import detect_skills


file_path = "backend/uploads/resume.pdf"


# Step 1: Resume text extract
resume_text = extract_resume_text(file_path)


# Step 2: Skills detect
skills = detect_skills(resume_text)


print("\n========== DETECTED SKILLS ==========\n")

for skill in skills:
    print("✓", skill)

print("\n=====================================\n")