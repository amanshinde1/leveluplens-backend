import re

SKILL_PRIORITY = {
    "python": "core",
    "django": "core",
    "java": "core",

    "sql": "secondary",
    "mysql": "secondary",
    "postgresql": "secondary",
    "api": "secondary",
    "rest": "secondary",
    "git": "secondary",

    "kafka": "advanced",
    "docker": "advanced",
    "kubernetes": "advanced",
    "clickhouse": "advanced"
}


def get_skill_weight(skill):
    level = SKILL_PRIORITY.get(skill, "secondary")

    if level == "core":
        return 1.0
    elif level == "secondary":
        return 0.7
    else:
        return 0.4

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
    "aws","gcp","azure","cloudformation","serverless",
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

SEMANTIC_PATTERNS = {
    "api": [
        "backend service",
        "backend services",
        "rest endpoint",
        "web service",
        "web services",
        "http service",
        "microservice",
        "microservices"
    ],
    "docker": [
        "containerized",
        "containerization"
    ],
    "kubernetes": [
        "orchestration",
        "container orchestration"
    ],
    "cicd": [
        "deployment pipeline",
        "build pipeline",
        "release pipeline"
    ]
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


    "rest services": "api",
    "container":"docker",
    "containerization":"docker",
    "rest": "api",
    "restful": "api",
    "agile":"agile",
    "microservices": "api",
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

    # normalize plurals / variants
    text = re.sub(r'\bapis\b', 'api', text)
    text = re.sub(r'\blambdas\b', 'lambda', text)
    text = re.sub(r'\bqueues\b', 'queue', text)
    text = re.sub(r'\bdatabases\b', 'database', text)
    text = re.sub(r'\bservices\b', 'service', text)
    text = re.sub(r'\brestful\b', 'rest', text)

    # canonical normalization
    for variant, canonical in CANONICAL_MAP.items():
        pattern = r'\b' + re.escape(variant) + r'\b'
        text = re.sub(pattern, canonical, text)

    # phrase normalization
    text = replace_phrase_skills(text)


    explicit_skills = set()
    inferred_skills = set()

    # =============================
    # 🔥 1. CONTEXT INFERENCE (IMPORTANT FIX)
    # =============================
    for phrase, skill in CONTEXT_SKILL_MAP.items():
        if phrase in text:
            inferred_skills.add(skill)

    # =============================
    # 🔥 2. SEMANTIC PATTERNS
    # =============================
    for skill, patterns in SEMANTIC_PATTERNS.items():
        for pattern in patterns:
            if pattern in text:
                inferred_skills.add(skill)

    # =============================
    # 🔥 3. EXACT MATCH
    # =============================
    for skill in TECH_SKILLS:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text):
            explicit_skills.add(normalize_skill(skill))

    return explicit_skills, inferred_skills


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
            "your skills",
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

    # normalize different dash types
    text = text.replace("–", "-").replace("—", "-")

    patterns = [

        # 1-4 years OR 1 - 4 years
        r'(\d+)\s*-\s*(\d+)\s*(?:years?|yrs?)',

        # 1 to 4 years
        r'(\d+)\s*to\s*(\d+)\s*(?:years?|yrs?)',

        # 4+ years
        r'(\d+)\+?\s*(?:years?|yrs?)'
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:

            nums = [int(n) for n in match.groups() if n]

            if len(nums) >= 2:
                return min(nums)   # ✅ ALWAYS lower bound

            return nums[0]  # single value case

    return None


def generate_reasoning(
    decision,
    matched_required,
    missing_required,
    total_required,
    required_experience,
    user_experience
):

    matched_list = list(matched_required)[:3]
    missing_list = list(missing_required)[:3]

    matched_str = ", ".join(matched_list) if matched_list else ""
    missing_str = ", ".join(missing_list) if missing_list else ""

    if decision == "APPLY":
        return (
            f"You meet most of the core requirements for this role"
            f"{f', including {matched_str}' if matched_str else ''}. "
            f"Your experience also aligns well with typical expectations."
        )

    if decision == "CONSIDER":
        return (
            f"You meet several key requirements"
            f"{f' such as {matched_str}' if matched_str else ''}, "
            f"but the role also expects skills like {missing_str}. "
            f"This suggests partial alignment with the role’s expectations, "
            f"which may affect your chances in more competitive applications."
        )

    if decision == "SKIP":

        if required_experience and user_experience < required_experience:
            return (
                f"This role typically expects around {required_experience} years of experience, "
                f"while your profile shows {user_experience}. "
                f"This gap may significantly impact your chances."
            )

        return (
            f"This role expects skills like {missing_str} which are not present in your profile. "
            f"Your current skill set does not fully align with the core expectations of this role."
        )

    return ""


def analyze_job(resume_skills, job_description, user_experience):

    job_description = job_description[:3000]

    # Normalize resume skills
    resume_skills = set(normalize_skill(s) for s in resume_skills)

    # =============================
    # EXTRACT SKILLS (NEW FIX)
    # =============================
    required_explicit, required_inferred = extract_unique_skills(job_description)
    required_skills = required_explicit | required_inferred

    nice_skills = set()

    # Fallback (safe)
    if not required_skills:
        fallback_explicit, fallback_inferred = extract_unique_skills(job_description)
        required_skills = fallback_explicit | fallback_inferred

    # Context inference (keep existing logic)
    context_skills = set(normalize_skill(s) for s in infer_context_skills(job_description))
    required_skills = required_skills.union(context_skills.intersection(TECH_SKILLS))

    # Normalize again (safety)
    required_skills = set(normalize_skill(s) for s in required_skills)
    nice_skills = set(normalize_skill(s) for s in nice_skills)

    # =============================
    # MATCHING
    # =============================
    matched_required = resume_skills & required_skills
    missing_required = required_skills - resume_skills
    matched_nice = resume_skills & nice_skills

    # 🔥 NEW: explicit vs inferred split
    matched_required_explicit = resume_skills & required_explicit
    matched_required_inferred = (resume_skills & required_inferred) - matched_required_explicit

    total_required = len(required_skills)
    total_nice = len(nice_skills)

    # =============================
    # SCORING
    # =============================
    def weighted_score(matched, total):
        if not total:
            return 0

        matched_weight = sum(get_skill_weight(s) for s in matched)
        total_weight = sum(get_skill_weight(s) for s in total)

        return (matched_weight / total_weight) * 100

    required_percent = weighted_score(matched_required, required_skills)
    nice_percent = weighted_score(matched_nice, nice_skills)

    base_score = (required_percent * 0.85) + (nice_percent * 0.15)
    final_score = base_score

    # =============================
    # PENALTIES
    # =============================
    critical_missing = [s for s in missing_required if get_skill_weight(s) == 1.0]
    critical_penalty = min(15, len(critical_missing) * 4)
    final_score -= critical_penalty

    match_ratio = len(matched_required) / max(1, len(required_skills))

    if match_ratio < 0.25:
        final_score *= 0.7
    elif match_ratio < 0.5:
        final_score *= 0.85

    # =============================
    # SENIOR PENALTY
    # =============================
    SENIOR_KEYWORDS = ["system design", "distributed", "scalable", "architecture"]

    jd_lower = job_description.lower()
    senior_signal = any(k in jd_lower for k in SENIOR_KEYWORDS)

    senior_penalty_applied = False

    if senior_signal and len(matched_required) < 3:
        final_score *= 0.75
        senior_penalty_applied = True

    # =============================
    # EDGE CASES
    # =============================
    if total_required == 0:
        final_score = max(final_score, 50)

    if total_required == 1:
        final_score = max(final_score, 40)

    final_score = max(0, min(final_score, 100))

    # =============================
    # DECISION
    # =============================
    if final_score >= 75:
        decision = "STRONG_APPLY"
    elif final_score >= 55:
        decision = "APPLY"
    elif final_score >= 35:
        decision = "CONSIDER"
    else:
        decision = "SKIP"

    # =============================
    # RISK
    # =============================
    if final_score >= 75:
        risk = "Strong Alignment"
    elif final_score >= 45:
        risk = "Moderate Alignment"
    else:
        risk = "Low Alignment"

    # =============================
    # EXPERIENCE
    # =============================
    required_experience = extract_required_experience(job_description)
    experience_block = False

    if required_experience and user_experience < required_experience:
        experience_block = True

    # =============================
    # CONFIDENCE
    # =============================
    low_signal = False

    if len(required_skills) < 3:
        low_signal = True

    if len(job_description.strip()) < 200:
        low_signal = True

    if low_signal:
        confidence = "LOW"
    elif len(required_skills) < 5:
        confidence = "MEDIUM"
    else:
        confidence = "HIGH"

    # =============================
    # GAPS
    # =============================
    critical_gaps = list(critical_missing)
    learnable_gaps = [s for s in missing_required if s not in critical_missing]

    # =============================
    # BREAKDOWN
    # =============================
    score_breakdown = {
        "required": {
            "matched": len(matched_required),
            "total": total_required,
            "percent": round(required_percent, 2),
        },
        "nice": {
            "matched": len(matched_nice),
            "total": total_nice,
            "percent": round(nice_percent, 2),
        },
        "penalties": {
            "critical_missing_count": len(critical_missing),
            "critical_penalty": critical_penalty,
            "low_match_penalty": match_ratio < 0.5,
            "senior_penalty": senior_penalty_applied
        }
    }

    # =============================
    # REASONING
    # =============================
    reasoning = generate_reasoning(
        decision,
        matched_required,
        missing_required,
        total_required,
        required_experience,
        user_experience
    )

    # =============================
    # FRICTION
    # =============================
    if risk == "Low Alignment":
        friction = "You may be competing with significantly stronger profiles."
    elif risk == "Moderate Alignment":
        friction = "You meet some requirements, but gaps may affect your chances."
    else:
        friction = "Your profile aligns well with this role."

    # =============================
    # LEARNING
    # =============================
    learning = ""

    if "django" in required_skills and "rest" in required_skills:
        learning = "Most backend roles expect both framework knowledge and API experience."
    elif "docker" in required_skills:
        learning = "Modern backend roles often expect deployment knowledge."
    elif "aws" in required_skills:
        learning = "Cloud experience is increasingly expected in backend roles."
    elif len(required_skills) > 8:
        learning = "This role has broad requirements, indicating higher competition."

    # =============================
    # ORDER
    # =============================
    matched_required_ordered = [
        skill for skill in required_skills if skill in resume_skills
    ]

    missing_required_ordered = [
        skill for skill in required_skills if skill not in resume_skills
    ]

    matched_nice_ordered = [
        skill for skill in nice_skills if skill in resume_skills
    ]

    # =============================
    # FINAL RESPONSE
    # =============================
    return {
        "match_score": round(final_score, 2),
        "confidence": confidence,
        "decision": decision,
        "risk": risk,

        "score_breakdown": score_breakdown,

        "resume_skills_detected": list(resume_skills),
        "job_skills_detected": list(required_skills | nice_skills),

        "critical_gaps": critical_gaps,
        "learnable_gaps": learnable_gaps,

        "friction": friction,
        "learning": learning,
        "reasoning": reasoning,

        "matched_required": matched_required_ordered,
        "matched_required_explicit": list(matched_required_explicit),
        "matched_required_inferred": list(matched_required_inferred),

        "missing_required": missing_required_ordered,
        "matched_nice": matched_nice_ordered,

        "required_experience": required_experience,
        "user_experience_years": user_experience,
        "experience_block": experience_block,

        "low_signal": low_signal,
    }