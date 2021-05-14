FROM openjdk:8-jdk-alpine

ADD view-api.jar /root
ADD application.properties /root

RUN mkdir -p /etc/configs/ && cd /root/

CMD ["/bin/sh", "-l", "-c", "java -jar /root/view-api.jar --spring.config.location=/root/application.properties"]

    
