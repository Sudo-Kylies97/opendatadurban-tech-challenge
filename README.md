# opendatadurban-tech-challenge


## 1. Scheduling the Scrapers to Run Daily

### Steps to run cron
1. **Dockerize the Scraper** 
2. **Push Docker Image to Amazon ECR**
3. **Create an ECS Task Definition for the Scraper**
4. **Create a CloudWatch Event Rule to Trigger the Scraper Daily**


## 2. FastAPI (Python web application framework) Deployment on AWS (cloud provider)

### Architecture

1. **Amazon ECS (Elastic Container Service) with Fargate**: For running Docker containers without managing servers.
2. **Amazon RDS (Relational Database Service)**: For managing the PostgreSQL database.
3. **AWS CloudWatch**: For monitoring logs and setting up alarms.
4. **Amazon ECR (Elastic Container Registry)**: For storing Docker images.
5. **AWS Secrets Manager**: For securely managing sensitive information such as database credentials.
6. **Application Load Balancer (ALB)**: For distributing incoming traffic across multiple ECS tasks.

### Deployment Steps

1. **Containerize the FastAPI Application**
2. **Push the Docker Image to Amazon ECR**
3. **Create an Amazon RDS PostgreSQL Database**
4. **Create an ECS Task Definition for FastAPI**
5. **Configure an Application Load Balancer**
6. **Deploy the ECS Service**
7. **Set Up CloudWatch for Monitoring**

## 3.  handle errors, downtime & alerts.

### Error Handling
1. **Use structured logging and capture exceptions.**
2. **Implement retries and circuit breakers.**
### Monitoring
1. **Use CloudWatch for metrics collection and monitoring.**
2. **Send logs to CloudWatch Logs for centralized log management.**
### Alerts
1. **Set up CloudWatch Alarms for critical metrics.**
2. **Use SNS for notifications and alerts.**
### Downtime Management
1. **Configure health checks and auto-scaling for ECS tasks.**
2. **Enable RDS automated backups and use Multi-AZ for high availability.**
3. **Set up disaster recovery strategies.**