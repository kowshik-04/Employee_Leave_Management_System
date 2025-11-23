pipeline {
    agent any

    environment {
        OPT_DIR = 'opt'
        REPORT_DIR = 'opt/output'
        HERCULES_IMAGE = 'testzeus/hercules:latest'
    }

    options {
        timestamps()
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '20'))
    }

    triggers {
        pollSCM('') // GitHub webhook still triggers automatically
    }

    stages {

        stage('Initialize') {
            steps {
                checkout scm
                sh '''
                    rm -rf ${OPT_DIR}
                    mkdir -p ${OPT_DIR}/input ${OPT_DIR}/output
                '''
            }
        }

        stage('Detect Changes') {
            steps {
                sh '''
                    PREV=""
                    if git rev-parse --verify HEAD^1 >/dev/null 2>&1; then PREV=$(git rev-parse HEAD^1); fi

                    if [ -z "$PREV" ]; then
                        git ls-files > changed_files.txt
                    else
                        git diff --name-only $PREV HEAD > changed_files.txt
                    fi

                    cp changed_files.txt ${REPORT_DIR}/
                '''
            }
        }

        stage('Run Hercules') {
            steps {
                withCredentials([string(credentialsId: 'OPENAI_API_KEY', variable: 'OPENAI_API_KEY')]) {
                    sh '''
                        docker run --rm \
                          -e OPENAI_API_KEY="${OPENAI_API_KEY}" \
                          -v "$PWD":/workspace \
                          -v "$PWD/${OPT_DIR}":/workspace/${OPT_DIR} \
                          -w /workspace \
                          ${HERCULES_IMAGE} \
                          bash -lc "testzeus-hercules --project-base=${OPT_DIR}" \
                          > ${REPORT_DIR}/hercules_stdout.log \
                          2> ${REPORT_DIR}/hercules_stderr.log || true
                    '''
                }
            }
        }

        stage('AI Analysis') {
            steps {
                withCredentials([string(credentialsId: 'OPENAI_API_KEY', variable: 'OPENAI_API_KEY')]) {
                    sh '''
                        python3 - <<'EOF'
import openai, json, os

openai.api_key = os.getenv("OPENAI_API_KEY")

stdout = open("opt/output/hercules_stdout.log", "r", errors="ignore").read()
stderr = open("opt/output/hercules_stderr.log", "r", errors="ignore").read()

prompt = f"""
You are an autonomous Test Evaluation Agent.

Analyze the following logs:

STDOUT:
{stdout}

STDERR:
{stderr}

Return JSON ONLY:
{{
"relevance_score": "",
"coverage_estimation": "",
"quality_rating": "",
"summary": "",
"issues": [],
"recommendations": []
}}
"""

resp = openai.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": prompt}],
)

analysis = resp.choices[0].message.content
open("opt/output/ai_analysis.json", "w").write(analysis)

EOF
                    '''
                }
            }
        }

        stage('Generate HTML Dashboard (C)') {
            steps {
                sh '''
                    python3 - << 'EOF'
import json, os

# load AI analysis
analysis = json.load(open("opt/output/ai_analysis.json"))

html = f"""
<html>
<head>
<title>Hercules AI Test Dashboard</title>
<style>
body {{ font-family: Arial; padding:20px; }}
h1 {{ color:#4CAF50; }}
pre {{ background:#f4f4f4; padding:10px; }}
</style>
</head>
<body>
<h1>Hercules Automated Test Report</h1>
<h2>Quality Rating: {analysis['quality_rating']}</h2>
<h3>Relevance Score: {analysis['relevance_score']}</h3>
<h3>Coverage Estimation: {analysis['coverage_estimation']}</h3>
<h3>Summary:</h3>
<pre>{analysis['summary']}</pre>
<h3>Issues:</h3>
<pre>{json.dumps(analysis['issues'], indent=2)}</pre>
<h3>Recommendations:</h3>
<pre>{json.dumps(analysis['recommendations'], indent=2)}</pre>
</body>
</html>
"""

open("opt/output/dashboard.html", "w").write(html)
EOF
                '''
            }
        }

        stage('Encrypt Results') {
            steps {
                withCredentials([file(credentialsId: 'USER_PGP_PUB', variable: 'USER_PGP_PUB_FILE')]) {
                    sh '''
                        tar -czf results_${BUILD_ID}.tar.gz opt/output
                        export GNUPGHOME=$(mktemp -d)
                        gpg --import "${USER_PGP_PUB_FILE}"

                        RECIPIENT=$(gpg --list-keys --with-colons | awk -F: '/^pub/ {print $5; exit}')

                        gpg --yes --trust-model always \
                            --output results_${BUILD_ID}.tar.gz.gpg \
                            --encrypt -r "$RECIPIENT" \
                            results_${BUILD_ID}.tar.gz

                        mv results_${BUILD_ID}.tar.gz.gpg opt/output/
                        rm -rf "$GNUPGHOME"
                    '''
                }
            }
        }

        stage('Archive Results') {
            steps {
                archiveArtifacts artifacts: 'opt/output/**', fingerprint: true
            }
        }
    }

    post {
        success {
            emailext (
                to: '2004kowshik@gmail.com',
                subject: "Hercules Agent Run: SUCCESS (Build ${BUILD_NUMBER})",
                body: "Your autonomous test pipeline has completed. The encrypted results are attached.",
                attachmentsPattern: "opt/output/*.gpg"
            )
        }
        failure {
            emailext (
                to: '2004kowshik@gmail.com',
                subject: "Hercules Agent Run: FAILED (Build ${BUILD_NUMBER})",
                body: "Your autonomous pipeline FAILED. Please check Jenkins logs."
            )
        }
    }
}
