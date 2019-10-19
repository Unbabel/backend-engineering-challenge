# Compilation
scalac -target:jvm-1.8 -d target/UnbabelCli-1.0.0.jar  src/main/scala/com/unbabel/*

# Execution
scala -classpath target/UnbabelCli-1.0.0.jar com.unbabel.UnbabelCli