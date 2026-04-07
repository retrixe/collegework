docker run --name service-db   -e MYSQL_ROOT_PASSWORD=password   -e MYSQL_DATABASE=ServicePortal   -p 3306:3306   -d mysql:latest
docker exec -it service-db mysql -u root -ppassword ServicePortal -e "CREATE TABLE IF NOT EXISTS requests (id INT AUTO_INCREMENT PRIMARY KEY, service_type VARCHAR(50), description TEXT, status VARCHAR(20) DEFAULT 'Pending');"
#docker run -it --name service-web   -p 8080:8080   --link service-db:mysql   -v $(pwd)/build/libs/java-1.0-SNAPSHOT.war:/usr/local/tomcat/webapps/ROOT.war   tomcat:10.1-jdk17
exec docker run -it --name service-web   --net=host   -v $(pwd)/build/libs/service-portal-1.0-SNAPSHOT.war:/usr/local/tomcat/webapps/ROOT.war:Z   tomcat:10.1-jdk17
