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
        durabilityHint('PERFORMANCE_OPTIMIZED')
    }

    triggers {
        // GitHub webhook triggers automatically
        pollSCM('')
    }

    stages {

        stage('🔍 Initialize Workspace') {
            steps {
                checkout scm
                sh '''
                    rm -rf ${OPT_DIR}
                    mkdir -p ${OPT_DIR}/input ${OPT_DIR}/output
                '''
            }
        }

        stage('📁 Detect File Changes (Autonomous)') {
            steps {
                script {
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
        }

        stage('🤖 Auto-Run Hercules (AI Agent Mode)') {

            steps {
                withCredentials([string(credentialsId: 'OPENAI_API_KEY', variable: 'OPENAI_API_KEY')]) {
                    sh '''
                        echo "=== AI Agent: Starting Hercules Autonomous Run ==="

                        docker run --rm \
                          -e OPENAI_API_KEY="${OPENAI_API_KEY}" \
                          -v "$PWD":/workspace \
                          -v "$PWD/${OPT_DIR}":/workspace/${OPT_DIR} \
                          -w /workspace \
                          ${HERCULES_IMAGE} \
                          bash -lc "testzeus-hercules --project-base=${OPT_DIR}" \
                          > ${REPORT_DIR}/hercules_stdout.log \
                          2> ${REPORT_DIR}/hercules_stderr.log || true

                        echo "=== AI Agent: Hercules Finished ==="
                    '''
                }
            }
        }

        stage('🧠 AI Evaluation of Test Quality (Fully Agentic)') {
            steps {
                withCredentials([string(credentialsId: 'OPENAI_API_KEY', variable: 'OPENAI_API_KEY')]) {

                    sh '''
                        echo "=== AI Agent: Evaluating Test Quality ==="

                        python3 - <<'EOF'
import openai, json, os

openai.api_key = os.getenv("OPENAI_API_KEY")

# Read hercules output logs
stdout = open("opt/output/hercules_stdout.log", "r", errors="ignore").read()
stderr = open("opt/output/hercules_stderr.log", "r", errors="ignore").read()

prompt = f"""
You are an autonomous Test Evaluation Agent.

Analyze the following Hercules logs:
STDOUT:
{stdout}

STDERR:
{stderr}

Evaluate:
1. Test relevance to modified files
2. Test code quality
3. Completeness of test coverage
4. Issues or failures
5. Recommendations

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

        stage('🔐 Encrypt Results (Owner-Only Access)') {
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

        stage('📦 Archive Results') {
            steps {
                archiveArtifacts artifacts: 'opt/output/**', fingerprint: true
            }
        }

    }

    post {
        always {
            echo "=== Autonomous Pipeline Completed ==="
        }
    }
}
