# Source this file: `source scripts/dev-env.sh`
# Pins the project to JDK 25 (Homebrew's default `openjdk` is a newer non-LTS release).
export JAVA_HOME=/opt/homebrew/opt/openjdk@25/libexec/openjdk.jdk/Contents/Home
export PATH="$JAVA_HOME/bin:/opt/homebrew/opt/postgresql@18/bin:$PATH"
