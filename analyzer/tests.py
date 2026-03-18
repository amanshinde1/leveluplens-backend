from analyzer.services import extract_unique_skills, analyze_job


# =============================
# SKILL EXTRACTION TESTS
# =============================

def test_rest_api_extraction():
    result = extract_unique_skills("Designed RESTful services")
    assert "rest" in result
    assert "api" in result


def test_microservices_maps_to_api():
    result = extract_unique_skills("Built microservices architecture")
    assert "api" in result


def test_docker_detection():
    result = extract_unique_skills("Containerized applications")
    assert "docker" in result


# =============================
# SCORING TESTS
# =============================

def test_strong_fit_score():
    result = analyze_job(
        ["python", "django", "api"],
        "Looking for Django developer with REST APIs",
        2
    )
    assert result["match_score"] >= 60


def test_low_fit_score():
    result = analyze_job(
        ["html", "css"],
        "Looking for backend engineer with Django and APIs",
        1
    )
    assert result["match_score"] < 50


# =============================
# SENIOR ROLE PENALTY TEST
# =============================

def test_senior_penalty_applied():
    result = analyze_job(
        ["python", "api"],
        "Requires system design and distributed systems",
        1
    )
    assert result["match_score"] < 60