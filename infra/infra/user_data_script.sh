#!/bin/bash

# Get admin privileges
sudo su

# Update the system
yum update -y

# Install required packages
yum install python3-pip -y
yum install python3 -y
yum install -y docker
yum install -y htop

# Add the current user to the docker group
usermod -a -G docker ec2-user

# Start and enable the Docker service
systemctl start docker.service
systemctl enable docker.service

# Install Docker Compose
curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Create the Airflow directories
mkdir -p /home/ec2-user/airflow/{dags,logs,plugins,config}

echo -e "AIRFLOW_UID=$(id -u ec2-user)" >> /home/ec2-user/airflow/.env

curl -Lf 'https://airflow.apache.org/docs/apache-airflow/2.9.0/docker-compose.yaml' -o /home/ec2-user/airflow/docker-compose.yaml

# Run the Airflow initialization
docker-compose -f /home/ec2-user/airflow/docker-compose.yaml up airflow-init

# Start the Airflow services
docker-compose -f /home/ec2-user/airflow/docker-compose.yaml up -d

# Create a Python virtual environment
python3 -m venv /home/ec2-user/.airflow_env
source /home/ec2-user/.airflow_env/bin/activate
pip install pandas s3fs sqlalchemy psycopg2-binary 

echo "Bye, CDK!" >> /home/ec2-user/user_data_test.txt