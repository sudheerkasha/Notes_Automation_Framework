pipeline {
agent any

parameters {
    choice(
        name: 'BROWSER',
        choices: ['chrome', 'firefox', 'edge'],
        description: 'Browser for UI tests'
    )

    choice(
        name: 'ENV',
        choices: ['dev', 'staging', 'production'],
        description: 'Target environment'
    )

    booleanParam(
        name: 'HEADLESS',
        defaultValue: true,
        description: 'Run browser in headless mode'
    )

    string(
        name: 'PARALLEL_WORKERS',
        defaultValue: '4',
        description: 'Number of parallel workers'
    )
}

environment {
    TEST_ENV = "${params.ENV}"
    BROWSER = "${params.BROWSER}"
    HEADLESS = "${params.HEADLESS}"
    PYTHONPATH = "${WORKSPACE}"
}

stages {

    stage('Checkout') {
        steps {
            checkout([
                $class: 'GitSCM',
                branches: [[name: '*/main']],
                userRemoteConfigs: [[
                    url: 'https://github.com/sudheerkasha/Notes_automation_Framework'
                ]]
            ])

            echo 'Code checked out successfully'
        }
    }

    stage('Verify Environment') {
        steps {
            sh '''
                pwd
                ls -la
                python3 --version
                which python3
            '''
        }
    }

    stage('Setup Environment') {
        steps {
            sh '''
                python3 -m venv venv
                . venv/bin/activate

                python --version
                pip install --upgrade pip

                mkdir -p reports
                mkdir -p reports/allure-results

                pip install -r requirements.txt
            '''
        }
    }

    stage('API Health Check') {
        steps {
            sh '''
                . venv/bin/activate

                python -c "
```

import requests
r=requests.get('https://practice.expandtesting.com/notes/api/health-check')
print('API Status:', r.status_code)
"
'''
}
}

    stage('Run Tests') {
        steps {
            sh '''
                . venv/bin/activate

                ls -la
                ls -la tests || true

                pytest tests \
                -v \
                -s \
                --junitxml=reports/results.xml \
                --alluredir=reports/allure-results \
                --reruns=2 \
                --reruns-delay=2
            '''
        }
    }

    stage('Generate Allure Report') {
        steps {
            allure(
                includeProperties: false,
                jdk: '',
                results: [[path: 'reports/allure-results']]
            )
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
    }

    success {
        echo 'All tests PASSED!'
    }

    failure {
        echo 'Tests FAILED. Check console and Allure report.'
    }

    cleanup {
        cleanWs()
    }
}


}
