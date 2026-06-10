pipeline {
    
agent any

parameters {

    choice(
        name: 'BROWSER',
        choices: ['chrome', 'firefox', 'edge'],
        description: 'Browser for UI tests'
    )

    booleanParam(
        name: 'HEADLESS',
        defaultValue: true,
        description: 'Run tests in headless mode'
    )
}

environment {
    PYTHONPATH = "${WORKSPACE}"
    TEST_BROWSER = "${params.BROWSER}"
    HEADLESS_MODE = "${params.HEADLESS}"
}

stages {

    stage('Clean Workspace') {
        steps {
            cleanWs()
            echo 'Workspace cleaned successfully'
        }
    }

    stage('Checkout Code') {
        steps {
            git(
                branch: 'main',
                url: 'https://github.com/sudheerkasha/NOTES_AUTOMATION_FRAMEWORK_CAP.git'
            )

            echo 'Repository cloned successfully'
        }
    }

    stage('Verify Environment') {
        steps {
            sh '''
                echo "===== WORKSPACE ====="
                pwd

                echo "===== FILES ====="
                ls -la
            '''
        }
    }

    stage('Setup Python Environment') {
        steps {
            sh '''
                python3 --version

                python3 -m venv venv

                . venv/bin/activate

                python -m pip install --upgrade pip

                pip install -r requirements.txt
            '''

            echo 'Python environment setup completed'
        }
    }

    stage('Collect Tests') {
        steps {
            sh '''
                . venv/bin/activate

                echo "===== PYTEST VERSION ====="
                pytest --version

                echo "===== COLLECT TESTS ====="
                pytest --collect-only -q
            '''
        }
    }

    stage('Run Tests') {
        steps {
            sh '''
                . venv/bin/activate

                mkdir -p reports
                rm -rf reports/allure-results

                pytest tests \
                -v \
                -s \
                --cache-clear \
                --junitxml=reports/results.xml \
                --alluredir=reports/allure-results
            '''
        }
    }

    stage('Generate Allure Report') {
        steps {
            script {
                if (fileExists('reports/allure-results')) {
                    allure(
                        includeProperties: false,
                        jdk: '',
                        results: [[path: 'reports/allure-results']]
                    )
                }
            }
        }
    }
}

post {

    always {

        archiveArtifacts(
            artifacts: 'reports/**/*',
            allowEmptyArchive: true
        )

        junit(
            testResults: 'reports/results.xml',
            allowEmptyResults: true
        )

        echo 'Reports archived successfully'
    }

    success {
        echo 'Pipeline executed successfully'
    }

    failure {
        echo 'Pipeline execution failed'
    }

    cleanup {
        cleanWs(
            deleteDirs: true,
            disableDeferredWipeout: true
        )
    }
}
}
