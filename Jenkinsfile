pipeline {
  agent any
  stages {
    stage('Test') {
      steps { sh 'PYTHONPATH=src python3 -m unittest discover -s tests -v' }
    }
    stage('Benchmark') {
      steps { sh 'PYTHONPATH=src python3 scripts/benchmark.py --runs 30' }
    }
    stage('Container build') {
      steps { sh 'docker build -t fasd-cost-framework:${BUILD_NUMBER} .' }
    }
  }
  post { always { archiveArtifacts artifacts: 'outputs/**', fingerprint: true } }
}
