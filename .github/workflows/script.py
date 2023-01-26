name: CI
'on':
  push:
    branches:
    - master
    tags-ignore:
    - armeria-*
  pull_request: null
concurrency:
  group: ci-${{ github.event.pull_request.number || github.sha }}
  cancel-in-progress: true
env:
  LC_ALL: en_US.UTF-8
jobs:
  lint:
    if: github.repository == 'line/armeria'
    runs-on: self-hosted
    timeout-minutes: 60
    steps:
    - uses: actions/checkout@v2
    - id: setup-jdk-17
      name: Set up JDK 17
      uses: actions/setup-java@v2
      with:
        distribution: temurin
        java-version: '17'
    - name: Run the linters
      run: './gradlew --no-daemon --stacktrace --max-workers=8 --parallel lint

        '
    - name: Clean up the cache
      run: 'rm -fr ~/.gradle/caches/[0-9]* || true

        rm -fr ~/.gradle/caches/journal-* || true

        rm -fr ~/.gradle/caches/transforms-* || true

        rm -f ~/.gradle/caches/*/*.lock || true

        rm -f ~/.gradle/caches/*/gc.properties || true

        '
      shell: bash
