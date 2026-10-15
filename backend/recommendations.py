
RECOMMENDATIONS = {
    "fastapi": {
        "priority": "High",
        "action": "Learn routing, request validation, response models, and error handling.",
        "project": "Build a resume-analysis API using FastAPI."
    },
    "rest api": {
        "priority": "High",
        "action": "Practise HTTP methods, JSON, status codes, and API validation.",
        "project": "Connect a React form to a Python REST API."
    },
    "nlp": {
        "priority": "High",
        "action": "Learn text preprocessing, tokenization, embeddings, and text classification.",
        "project": "Build a semantic job-search application."
    },
    "docker": {
        "priority": "High",
        "action": "Learn images, containers, Dockerfiles, volumes, and Compose.",
        "project": "Containerize the Resume Intelligence application."
    },
    "aws": {
        "priority": "Medium",
        "action": "Learn IAM basics, deployment, environment variables, and CloudWatch.",
        "project": "Deploy a small API to AWS."
    },
    "python": {
        "priority": "High",
        "action": "Practise functions, data structures, exceptions, and testing.",
        "project": "Build a tested data-processing pipeline."
    },
    "sql": {
        "priority": "High",
        "action": "Practise joins, grouping, filtering, and database design.",
        "project": "Build a job and application tracking database."
    },
    "machine learning": {
        "priority": "High",
        "action": "Practise feature engineering, model selection, and evaluation.",
        "project": "Compare classification models on a public dataset."
    },
    "scikit-learn": {
        "priority": "High",
        "action": "Practise preprocessing pipelines and model evaluation.",
        "project": "Build and evaluate a reproducible ML pipeline."
    },
    "pandas": {
        "priority": "Medium",
        "action": "Practise data cleaning, grouping, merging, and missing-value handling.",
        "project": "Analyse a public dataset and document your findings."
    },
    "numpy": {
        "priority": "Medium",
        "action": "Practise arrays, vectorization, indexing, and numerical operations.",
        "project": "Implement simple numerical operations and compare their performance."
    },
    "react": {
        "priority": "High",
        "action": "Practise components, props, state, hooks, and API calls.",
        "project": "Build an interactive job-matching dashboard."
    },
    "git": {
        "priority": "Medium",
        "action": "Practise branches, commits, merging, and pull requests.",
        "project": "Maintain a project repository with a clear commit history."
    },
    "deep learning": {
        "priority": "High",
        "action": "Learn neural networks, training loops, loss functions, and evaluation.",
        "project": "Train and evaluate a small neural network."
    },
    "tensorflow": {
        "priority": "Medium",
        "action": "Practise model building, training, and evaluation.",
        "project": "Train a classification model with TensorFlow."
    }
}


def recommend_skills(missing_skills: list[str]) -> list[dict]:
    recommendations = []

    for skill in missing_skills:
        key = skill.lower()
        details = RECOMMENDATIONS.get(key)

        if details:
            recommendations.append({
                "skill": skill,
                **details
            })
        else:
            recommendations.append({
                "skill": skill,
                "priority": "Medium",
                "action": f"Learn and practise {skill}.",
                "project": f"Build a small project using {skill}."
            })

    return recommendations
