plugins {
    id("java")
    id("application")
    id("com.gradleup.shadow") version "9.2.2"
}

group = "xyz.retrixe.collegework"
version = "1.0-SNAPSHOT"

application {
    mainClass = "xyz.retrixe.collegework.Main"
}

repositories {
    mavenCentral()
}

dependencies {
    implementation("org.apache.kafka:kafka-streams:4.1.0")
    implementation("com.maxmind.db:maxmind-db:3.2.0")
}

tasks.test {
    useJUnitPlatform()
}
