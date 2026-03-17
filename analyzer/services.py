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
    "node js":"node",
    "reactjs":"react",
    "react.js":"react",
    "js":"javascript",
    "py":"python",
    "postgres":"postgresql",
    "psql":"postgresql",
    "k8s":"kubernetes",
    "tf":"terraform",
    "aws cloud":"aws",
    "amazon web services":"aws",
    "google cloud":"gcp",
    "restful":"rest",
    "python3": "python",
    "py3": "python",
    "react.js": "react",
    "docker containers": "docker",
    "node js": "node",
    "aws cloud": "aws"
}


TECH_SKILLS = {

    # Languages
    "python","java","javascript","typescript","c","cpp","csharp",
    "go","golang","rust","scala","kotlin","swift","php","ruby","matlab","r","bash","powershell",

    # Backend frameworks
    "django","flask","fastapi","spring","springboot","express","node","nestjs",
    "laravel","rails","adonis","micronaut","quarkus","ktor","vertx",

    # Frontend
    "react","angular","vue","nextjs","nuxt","svelte","solidjs",
    "redux","zustand","vite","webpack","babel","eslint","storybook",
    "html","css","tailwind","bootstrap","materialui","mui","chakraui",

    # Databases
    "postgresql","mysql","mongodb","redis","sqlite","cassandra",
    "dynamodb","elasticsearch","neo4j","sql","plsql","oracle",
    "mariadb","cockroachdb","timescaledb","influxdb","clickhouse",
    "bigquery","redshift",

    # Cloud
    "aws","gcp","azure","cloudformation","serverless","cloud",
    "lambda","ec2","s3","eks","ecs","fargate",
    "cloudrun","cloudfunctions","cloudbuild",

    # DevOps
    "docker","kubernetes","terraform","ansible",
    "jenkins","cicd","github","gitlab","bitbucket",
    "helm","argo","prometheus","grafana",
    "circleci","travis","teamcity","spinnaker",
    "vault","consul","istio","linkerd",

    # Data Engineering
    "spark","hadoop","kafka","airflow","hive",
    "snowflake","databricks","presto","trino",
    "dbt","beam","flink","kinesis","delta","lakehouse",

    # Machine Learning
    "tensorflow","pytorch","scikit","opencv",
    "pandas","numpy","xgboost","lightgbm",
    "keras","huggingface","langchain","mlflow","onnx",

    # APIs
    "rest","api","graphql","grpc","soap",

    # Systems
    "linux","unix","shell","git",

    # Testing
    "pytest","junit","selenium","cypress","playwright",
    "mocha","chai","jest","vitest","karma",

    # Security
    "oauth","jwt","saml","tls","ssl",

    # Mobile
    "android","ios","reactnative","flutter",

    # Messaging
    "rabbitmq","activemq","nats",

    # Search
    "solr","lucene",

    # Concepts
    "ml","dl","nlp","cv","oop","designpatterns","unittest",
    "microservices","distributed","eventdriven","concurrency","multithreading",

    # Methodologies
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
    "event driven architecture":"eventdriven",
    "distributed systems":"distributed",
    "data pipelines":"airflow",
    "continuous integration":"cicd",
    "continuous delivery":"cicd",
    "container orchestration":"kubernetes"
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

    "event streaming":"kafka",

    "cloud platform":"cloud",

    "agile":"agile",
    "microservices": "docker",
    "data pipeline": "airflow",
    "event streaming": "kafka"
}


def normalize_skill(skill):
    skill = skill.lower().strip()
    return CANONICAL_MAP.get(skill, skill)


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

    # normalize punctuation before scanning
    text = text.lower()
    text = re.sub(r'[\/\-\.,&]', ' ', text)
    text = text.replace(" or ", " ")
    text = text.replace(" and ", " ")
    text = re.sub(r'\s+', ' ', text)

    # ---- ADD THIS BLOCK HERE ----
    text = re.sub(r'\bapis\b', 'api', text)
    text = re.sub(r'\blambdas\b', 'lambda', text)
    text = re.sub(r'\bqueues\b', 'queue', text)
    text = re.sub(r'\bdatabases\b', 'database', text)
    text = re.sub(r'\bservices\b', 'service', text)
    # -----------------------------

    for variant, canonical in CANONICAL_MAP.items():
        pattern = r'\b' + re.escape(variant) + r'\b'
        text = re.sub(pattern, canonical, text)

    text = replace_phrase_skills(text)

    found_skills = set()

    for skill in TECH_SKILLS:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text):
            found_skills.add(normalize_skill(skill))

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
            "skills required","key skills",
            "skills and experience",
            "your skills","experience",
            "tech stack",
            "technology stack",
            "your skills include",
            "skills include"
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


def extract_required_experience(text):

    text = text.lower()

    patterns = [

    # experience before numbers
    r'(?:experience|exp).{0,20}(\d+)\s*-\s*(\d+)\s*(?:years?|yrs?)',

    # number range
    r'(\d+)\s*-\s*(\d+)\s*(?:years?|yrs?)',

    # 5+ years
    r'(\d+)\+?\s*(?:years?|yrs?).{0,20}(?:experience|exp)',

    # experience ... 5 years
    r'(?:experience|exp).{0,20}(\d+)\+?\s*(?:years?|yrs?)'
]

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            nums = [int(n) for n in match.groups() if n]
            return min(nums)

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
                f"You already have several key skills such as {matched_str}. "
                f"Your experience also aligns well with the expectations of this role."
            )

        return "Your profile aligns well with this role."

    if decision == "CONSIDER":

        if matched_str:
            return (
                f"You already have some relevant skills including {matched_str}. "
                f"However the role also expects technologies like {missing_str}."
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
                f"However the role also expects technologies like {missing_str}."
            )

        return "This role currently requires several skills that are not present in your profile."

    return ""


def analyze_job(resume_skills, job_description, user_experience):

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

    min_required_matches = max(2, int(len(required_skills) * 0.3))

    if len(matched_required) < min_required_matches:
        final_score *= 0.6

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