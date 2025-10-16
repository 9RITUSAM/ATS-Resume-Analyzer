import re
from fuzzywuzzy import fuzz

BASE_SKILLS = [
    "python", "java", "c++", "javascript", "react", "node", "sql",
    "mongodb", "docker", "kubernetes", "linux", "git", "aws", "azure",
    "machine learning", "deep learning", "nlp", "pandas", "numpy",
]

STANDARD_SECTIONS = ["contact", "education", "experience", "skills", "projects"]


def clean_text(text):
    text = re.sub(r"\s+", " ", text).strip()
    return text


def split_sections(text):
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    sections = {}
    cur = "header"
    sections[cur] = []
    headings = set(STANDARD_SECTIONS + ["summary", "objective", "certifications"])
    for line in lines:
        low = line.lower().strip(": ")
        if low in headings or any(h in low for h in headings):
            cur = low
            sections[cur] = []
        else:
            sections.setdefault(cur, []).append(line)
    for k in list(sections.keys()):
        sections[k] = "\n".join(sections[k])
    return sections


def extract_skills(text, skill_list=BASE_SKILLS, threshold=80):
    found = set()
    t = text.lower()
    for s in skill_list:
        if s in t:
            found.add(s)
    words = re.findall(r"[a-zA-Z\+\#\-\.\d]+", t)
    for s in skill_list:
        for w in words:
            if fuzz.partial_ratio(s, w) >= threshold:
                found.add(s)
                break
    return sorted(found)


def ats_score(resume_text, jd_text="", experience_years=1, education_level="bachelors"):
    sections = split_sections(resume_text)
    skills_found = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text.lower()) if jd_text else []

   
    intersect = set(skills_found).intersection(set(jd_skills))
    skill_score = len(intersect) / max(len(jd_skills), 1) if jd_skills else 1

   
    found_sections = [s for s in STANDARD_SECTIONS if sections.get(s)]
    section_score = len(found_sections) / len(STANDARD_SECTIONS)

 
    exp_map = {"intern": 0.2, "0-1": 0.4, "1-3": 0.6, "3-5": 0.8, "5+": 1.0}
    if experience_years >= 5:
        exp_score = exp_map["5+"]
    elif experience_years >= 3:
        exp_score = exp_map["3-5"]
    elif experience_years >= 1:
        exp_score = exp_map["1-3"]
    elif experience_years > 0:
        exp_score = exp_map["0-1"]
    else:
        exp_score = exp_map["intern"]

 
    edu_map = {"phd":1.0, "masters":0.9, "bachelors":0.8, "diploma":0.6, "highschool":0.3}
    edu_score = edu_map.get(education_level.lower(), 0.5)

   
    total = skill_score*0.6 + section_score*0.2 + (exp_score+edu_score)*0.2/2
    total = round(total*100,1)

    missing_sections = list(set(STANDARD_SECTIONS) - set(found_sections))
    missing_skills = list(set(jd_skills) - set(skills_found)) if jd_skills else []

    return {
        "total_score": total,
        "skill_score": round(skill_score*100,1),
        "section_score": round(section_score*100,1),
        "experience_score": round(exp_score*100,1),
        "education_score": round(edu_score*100,1),
        "missing_sections": missing_sections,
        "missing_skills": missing_skills
    }
