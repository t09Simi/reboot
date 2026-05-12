from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify

from concepts.models import Skill, SkillCategory


# Curated taxonomy: category name → list of (canonical_name, slug, [aliases])
# Explicit slugs prevent collisions for names with special characters (C#, C++, .NET, etc.)
SKILL_TAXONOMY = {
    "Languages": [
        ("Python",       "python",       ["py", "python3"]),
        ("Java",         "java",         []),
        ("JavaScript",   "javascript",   ["js"]),
        ("TypeScript",   "typescript",   ["ts"]),
        ("Go",           "go",           ["golang"]),
        ("Ruby",         "ruby",         []),
        ("C#",           "csharp",       ["c sharp", "c-sharp"]),
        ("C++",          "cpp",          ["cplusplus", "c plus plus"]),
        ("PHP",          "php",          []),
        ("Kotlin",       "kotlin",       []),
        ("Swift",        "swift",        []),
        ("Rust",         "rust",         []),
        ("Scala",        "scala",        []),
        ("R",            "r-lang",       ["r language"]),
        ("SQL",          "sql",          []),
        ("Bash",         "bash",         ["shell", "shell scripting"]),
    ],
    "Frontend": [
        ("React",        "react",        ["react.js", "reactjs"]),
        ("Vue",          "vue",          ["vue.js", "vuejs"]),
        ("Angular",      "angular",      []),
        ("Next.js",      "nextjs",       ["next js"]),
        ("Nuxt",         "nuxt",         ["nuxt.js"]),
        ("HTML",         "html",         ["html5"]),
        ("CSS",          "css",          ["css3"]),
        ("Tailwind CSS", "tailwind-css", ["tailwind", "tailwindcss"]),
        ("Bootstrap",    "bootstrap",    []),
        ("Redux",        "redux",        []),
        ("Webpack",      "webpack",      []),
        ("Vite",         "vite",         []),
    ],
    "Backend": [
        ("Django",        "django",        []),
        ("Flask",         "flask",         []),
        ("FastAPI",       "fastapi",       ["fast api"]),
        ("Spring Boot",   "spring-boot",   ["spring", "springboot"]),
        ("Express",       "express",       ["express.js", "expressjs"]),
        ("Node.js",       "nodejs",        ["node", "node js"]),
        ("Ruby on Rails", "rails",         ["ror", "ruby on rails"]),
        (".NET",          "dotnet",        ["asp.net", "asp net", "net"]),
        ("NestJS",        "nestjs",        ["nest.js", "nest js"]),
        ("Laravel",       "laravel",       []),
    ],
    "Databases": [
        ("PostgreSQL",            "postgresql",  ["postgres"]),
        ("MySQL",                 "mysql",       []),
        ("SQLite",                "sqlite",      []),
        ("MongoDB",               "mongodb",     ["mongo"]),
        ("Redis",                 "redis",       []),
        ("Elasticsearch",         "elasticsearch", ["elastic search", "elastic"]),
        ("DynamoDB",              "dynamodb",    []),
        ("Cassandra",             "cassandra",   []),
        ("Oracle",                "oracle",      []),
        ("Microsoft SQL Server",  "mssql",       ["sql server", "ms sql"]),
    ],
    "Cloud": [
        ("AWS",          "aws",          ["amazon web services"]),
        ("Azure",        "azure",        ["microsoft azure"]),
        ("GCP",          "gcp",          ["google cloud", "google cloud platform"]),
        ("EC2",          "ec2",          []),
        ("S3",           "s3",           []),
        ("Lambda",       "aws-lambda",   ["aws lambda"]),
        ("RDS",          "rds",          []),
        ("CloudFront",   "cloudfront",   []),
        ("Heroku",       "heroku",       []),
        ("Vercel",       "vercel",       []),
        ("Netlify",      "netlify",      []),
        ("Railway",      "railway",      []),
    ],
    "DevOps": [
        ("Docker",         "docker",         []),
        ("Kubernetes",     "kubernetes",     ["k8s"]),
        ("Jenkins",        "jenkins",        []),
        ("GitHub Actions", "github-actions", []),
        ("GitLab CI",      "gitlab-ci",      ["gitlab cicd"]),
        ("CircleCI",       "circleci",       ["circle ci"]),
        ("Terraform",      "terraform",      []),
        ("Ansible",        "ansible",        []),
        ("Nginx",          "nginx",          []),
        ("Apache",         "apache",         []),
        ("Linux",          "linux",          []),
        ("CI/CD",          "cicd",           ["ci cd"]),
    ],
    "Data & ML": [
        ("Pandas",       "pandas",       []),
        ("NumPy",        "numpy",        []),
        ("TensorFlow",   "tensorflow",   ["tensor flow"]),
        ("PyTorch",      "pytorch",      ["py torch"]),
        ("Scikit-learn", "scikit-learn", ["sklearn"]),
        ("Spark",        "spark",        ["apache spark", "pyspark"]),
        ("Kafka",        "kafka",        ["apache kafka"]),
        ("Airflow",      "airflow",      ["apache airflow"]),
        ("Snowflake",    "snowflake",    []),
        ("Databricks",   "databricks",   []),
        ("Hadoop",       "hadoop",       []),
        ("Tableau",      "tableau",      []),
        ("Power BI",     "power-bi",     ["powerbi"]),
        ("LLMs",         "llms",         ["large language models", "llm"]),
        ("LangChain",    "langchain",    ["lang chain"]),
    ],
    "APIs & Architecture": [
        ("REST API",                  "rest-api",      ["rest", "restful", "rest apis", "restful api"]),
        ("GraphQL",                   "graphql",       ["graph ql"]),
        ("gRPC",                      "grpc",          []),
        ("WebSockets",                "websockets",    ["websocket", "web socket"]),
        ("Microservices",             "microservices", ["microservice"]),
        ("Event-Driven Architecture", "event-driven",  ["event driven"]),
        ("Serverless",                "serverless",    []),
    ],
    "Tools & Practices": [
        ("Git",         "git",         []),
        ("GitHub",      "github",      []),
        ("GitLab",      "gitlab",      []),
        ("Bitbucket",   "bitbucket",   []),
        ("Postman",     "postman",     []),
        ("Jira",        "jira",        []),
        ("Confluence",  "confluence",  []),
        ("Agile",       "agile",       []),
        ("Scrum",       "scrum",       []),
        ("TDD",         "tdd",         ["test driven development"]),
        ("BDD",         "bdd",         ["behavior driven development"]),
    ],
    "Testing": [
        ("Pytest",     "pytest",     ["py test"]),
        ("Jest",       "jest",       []),
        ("JUnit",      "junit",      ["j unit"]),
        ("Selenium",   "selenium",   []),
        ("Cypress",    "cypress",    []),
        ("Playwright", "playwright", []),
    ],
}


class Command(BaseCommand):
    help = "Seed the canonical Skill and SkillCategory tables. Idempotent."

    def add_arguments(self, parser):
        parser.add_argument(
            '--wipe',
            action='store_true',
            help='Delete all existing skills and categories before seeding.'
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options['wipe']:
            self.stdout.write(self.style.WARNING("Wiping existing skills and categories..."))
            Skill.objects.all().delete()
            SkillCategory.objects.all().delete()

        # Sanity check: ensure no slug collisions in the taxonomy itself
        all_slugs = []
        for skills in SKILL_TAXONOMY.values():
            all_slugs.extend(slug for _, slug, _ in skills)
        duplicates = {s for s in all_slugs if all_slugs.count(s) > 1}
        if duplicates:
            self.stdout.write(self.style.ERROR(
                f"Slug collisions in taxonomy: {duplicates}. Fix seed data before running."
            ))
            return

        category_count = 0
        skill_created = 0
        skill_updated = 0

        for order, (category_name, skills) in enumerate(SKILL_TAXONOMY.items()):
            category, created = SkillCategory.objects.update_or_create(
                name=category_name,
                defaults={'order': order}
            )
            if created:
                category_count += 1

            for skill_name, skill_slug, aliases in skills:
                _, created = Skill.objects.update_or_create(
                    slug=skill_slug,                       # ← lookup by slug (the unique key)
                    defaults={
                        'name': skill_name,
                        'aliases': aliases,
                        'category': category,
                    }
                )
                if created:
                    skill_created += 1
                else:
                    skill_updated += 1

        self.stdout.write(self.style.SUCCESS(
            f"Done. Categories created: {category_count}. "
            f"Skills created: {skill_created}. Skills updated: {skill_updated}."
        ))