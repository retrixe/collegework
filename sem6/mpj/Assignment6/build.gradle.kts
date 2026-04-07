import org.gradle.kotlin.dsl.dependencies

plugins {
    id("java")
    id("war")
}

group = "xyz.retrixe"
version = "1.0-SNAPSHOT"

java {
    sourceCompatibility = JavaVersion.VERSION_17 // 1_8
    targetCompatibility = JavaVersion.VERSION_17 // 1_8
}

/*application {
    mainClass = "xyz.retrixe.Main"
}*/

repositories {
    mavenCentral()
}

dependencies {
    // Jakarta Servlet API for 2026 (Tomcat 10+)
    compileOnly("jakarta.servlet:jakarta.servlet-api:6.0.0")
    implementation("com.mysql:mysql-connector-j:9.0.0")

    testImplementation(platform("org.junit:junit-bom:5.10.0"))
    testImplementation("org.junit.jupiter:junit-jupiter")
    testRuntimeOnly("org.junit.platform:junit-platform-launcher")
}

tasks.test {
    useJUnitPlatform()
}
