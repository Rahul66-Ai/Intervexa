from utils.resume_parser import extract_resume_text


file_path = "backend/uploads/resume.pdf"

text = extract_resume_text(file_path)

print("\n========== RESUME TEXT ==========\n")
print(text)
print("\n========== END ==========\n")