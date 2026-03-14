import re


STOP_WORDS = {
    "and","or","the","a","an",
    "in","with","of","to","for",
    "is","are","must","should",
    "strong","experience","knowledge",
    "looking","required","candidate",
    "role","team","we","have","nice",
    "build","write","development",
    "responsibilities","maintain",
    "maintainable","clean","code",
    "database","developer","engineer",
    "backend","frontend","design",
    "performance","scalable",
    "systems","optimize"
}


CANONICAL_MAP = {
    "apis":"api",
    "ci":"cicd",
    "cd":"cicd",
    "c++":"cpp",
    "cplusplus":"cpp",
    "nodejs":"node",
    "node.js":"node",
    "restful":"rest"
}


TECH_SKILLS = {

    "python","java","javascript","typescript","c","cpp","csharp",
    "go","golang","rust","scala","kotlin","swift","php","ruby","matlab","r",

    "django","flask","fastapi","spring","springboot",
    "express","node","nestjs","laravel","rails",

    "react","angular","vue","nextjs","nuxt","html","css","tailwind","bootstrap",

    "postgresql","mysql","mongodb","redis","sqlite",
    "cassandra","dynamodb","elasticsearch","neo4j","sql","plsql","oracle",

    "aws","gcp","azure","cloudformation","serverless","cloud",

    "docker","kubernetes","terraform","ansible",
    "jenkins","cicd","github","gitlab","bitbucket",
    "helm","argo","prometheus","grafana",

    "spark","hadoop","kafka","airflow","hive",
    "snowflake","databricks","presto","trino",

    "tensorflow","pytorch","scikit","opencv",
    "pandas","numpy","xgboost","lightgbm",

    "rest","api","graphql","grpc","soap",

    "linux","unix","bash","shell","git",

    "pytest","junit","selenium","cypress","playwright",

    "oauth","jwt","saml","tls","ssl",

    "android","ios","reactnative","flutter",

    "rabbitmq","activemq","nats",

    "solr","lucene",

    "ml","dl","nlp","cv","oop","designpatterns","unittest",

    "agile"
}


PHRASE_SKILLS = {
    "machine learning":"ml",
    "deep learning":"dl",
    "spring boot":"springboot",
    "google cloud platform":"gcp",
    "amazon web services":"aws",
    "react native":"reactnative",
    "natural language processing":"nlp",
    "computer vision":"cv",
    "design patterns":"designpatterns",
    "object oriented programming":"oop",
    "unit testing":"unittest",
    "rest api":"rest",
    "rest apis":"rest",
}


CONTEXT_SKILL_MAP = {
    "unit test":"unittest",
    "integration test":"unittest",
    "debugging":"unittest",
    "testing":"unittest",

    "deployment":"cicd",
    "deploy":"cicd",
    "release pipeline":"cicd",

    "microservice":"api",
    "rest service":"rest",
    "restful service":"rest",

    "container":"docker",
    "containerization":"docker",

    "agile":"agile",

    "cloud platform":"cloud",
}



def infer_context_skills(text):

    text = text.lower()

    inferred = set()

    for phrase, skill in CONTEXT_SKILL_MAP.items():

        if phrase in text:
            inferred.add(skill)

    return inferred



def replace_phrase_skills(text):

    text_lower = text.lower()

    for phrase, canonical in PHRASE_SKILLS.items():
        text_lower = text_lower.replace(phrase, canonical)

    return text_lower



def extract_unique_skills(text):

    text = replace_phrase_skills(text).lower()

    found_skills = set()

    for skill in TECH_SKILLS:

        pattern = r'\b' + re.escape(skill) + r'\b'

        if re.search(pattern, text):
            found_skills.add(skill)

    return found_skills



def extract_jd_sections(job_description):

    lines = job_description.lower().split("\n")

    required_section = []
    nice_section = []

    current_section = "neutral"

    for line in lines:

        if any(keyword in line for keyword in [
            "required","requirements",
            "must have","minimum qualifications",
            "qualifications","technical skills",
            "skills required","key skills"
        ]):
            current_section = "required"
            continue

        if any(keyword in line for keyword in [
            "nice to have","preferred",
            "good to have","plus","bonus"
        ]):
            current_section = "nice"
            continue

        if current_section == "required":
            required_section.append(line)

        elif current_section == "nice":
            nice_section.append(line)

    required_text = " ".join(required_section)
    nice_text = " ".join(nice_section)

    required_skills = extract_unique_skills(required_text)
    nice_skills = extract_unique_skills(nice_text)

    return required_skills, nice_skills



def normalize_skill(skill):

    skill = skill.lower().strip()

    replacements = {
        "restful api":"rest",
        "restful apis":"rest",
        "rest apis":"rest",
        "node.js":"node",
        "node js":"node",
        "structured query language":"sql",
        "amazon web services":"aws",
        "google cloud platform":"gcp",
        "docker containers":"docker"
    }

    return replacements.get(skill, skill)



def extract_required_experience(text):

    patterns = [
        r'(\d+)\+?\s*years',
        r'(\d+)\s*-\s*(\d+)\s*years'
    ]

    text = text.lower()

    for pattern in patterns:

        match = re.search(pattern, text)

        if match:

            if len(match.groups()) == 2:
                return int(match.group(2))

            return int(match.group(1))

    return None



def generate_reasoning(
    decision,
    matched_required,
    missing_required,
    total_required,
    required_experience,
    user_experience
):

    matched_list = sorted(list(matched_required))[:3]
    missing_list = sorted(list(missing_required))[:3]

    matched_str = ", ".join(matched_list) if matched_list else ""
    missing_str = ", ".join(missing_list) if missing_list else "other technologies"

    if decision == "APPLY":

        if matched_str:
            return (
                f"You match most of the required skills including {matched_str}. "
                f"Your experience also aligns well with the expectations of this role."
            )

        return "Your profile aligns well with this role."


    if decision == "CONSIDER":

        if matched_str:
            return (
                f"You match some important skills including {matched_str}. "
                f"However, technologies like {missing_str} are also mentioned in the role."
            )

        return "Your profile partially aligns with this role."


    if decision == "SKIP":

        if required_experience and required_experience > user_experience:
            return (
                f"This role expects around {required_experience} years of experience "
                f"while your profile shows {user_experience} years."
            )

        if matched_str:
            return (
                f"You match {len(matched_required)} required skills including {matched_str}. "
                f"However, technologies like {missing_str} are also required."
            )

        return "This role currently requires several skills that are not present in your profile."

    return ""



def analyze_job(resume_skills, job_description, user_experience):

    # prevent extremely large JD processing
    job_description = job_description[:3000]

    resume_skills = set(normalize_skill(s) for s in resume_skills)

    required_skills, nice_skills = extract_jd_sections(job_description)

    if not required_skills:
        required_skills = extract_unique_skills(job_description)

    context_skills = set(normalize_skill(s) for s in infer_context_skills(job_description))

    required_skills = required_skills.union(context_skills)

    required_skills = set(normalize_skill(s) for s in required_skills)
    nice_skills = set(normalize_skill(s) for s in nice_skills)


    matched_required = resume_skills & required_skills
    missing_required = required_skills - resume_skills

    matched_nice = resume_skills & nice_skills


    total_required = len(required_skills)
    total_nice = len(nice_skills)


    required_percent = (
        (len(matched_required) / total_required) * 100
        if total_required > 0 else 0
    )

    nice_percent = (
        (len(matched_nice) / total_nice) * 100
        if total_nice > 0 else 0
    )


    final_score = (required_percent * 0.8) + (nice_percent * 0.2)
    final_score = min(final_score, 100)


    if total_required == 0:
        final_score = max(final_score, 50)

    if total_required == 1:
        final_score = max(final_score, 40)


    if final_score >= 70:
        decision = "APPLY"
    elif final_score >= 40:
        decision = "CONSIDER"
    else:
        decision = "SKIP"


    required_experience = extract_required_experience(job_description)

    experience_block = False

    if required_experience and user_experience + 2 < required_experience:
        decision = "SKIP"
        experience_block = True


    reasoning = generate_reasoning(
        decision,
        matched_required,
        missing_required,
        total_required,
        required_experience,
        user_experience
    )


    return {
        "match_score": round(final_score, 2),
        "decision": decision,
        "reasoning": reasoning,
        "matched_required": sorted(list(matched_required)),
        "missing_required": sorted(list(missing_required)),
        "matched_nice": sorted(list(matched_nice)),
        "required_experience": required_experience,
        "user_experience_years": user_experience,
        "experience_block": experience_block
    }