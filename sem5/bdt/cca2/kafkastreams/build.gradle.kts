plugins {
    id("java")
}

group = "xyz.retrixe.collegework"
version = "1.0-SNAPSHOT"

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
