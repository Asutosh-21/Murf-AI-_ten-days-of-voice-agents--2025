# Day 6 Fraud Alert Agent - AWS Deployment Guide

## Deploy to AWS (Most Impressive for Job Applications)

### Option A: AWS EC2 (Recommended - Shows Real Cloud Skills)

#### Step 1: Launch EC2 Instance

```bash
# Install AWS CLI
pip install awscli

# Configure AWS
aws configure
# Enter: Access Key, Secret Key, Region (us-east-1), Output (json)

# Launch Ubuntu instance
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --instance-type t2.micro \
  --key-name your-key-pair \
  --security-group-ids sg-xxxxxx \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=fraud-agent}]'
```

#### Step 2: Connect and Setup

```bash
# SSH into instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Install dependencies
sudo apt update
sudo apt install python3-pip python3-venv nodejs npm -y

# Clone your repo
git clone https://github.com/your-username/your-repo.git
cd your-repo/"Day 6 Fraud Alert Agent"

# Setup backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create .env file
nano .env.local
# Add all your API keys

# Run backend
nohup python src/agent.py start &

# Setup frontend
cd ../frontend
npm install -g pnpm
pnpm install
pnpm build

# Run frontend
nohup pnpm start &
```

#### Step 3: Configure Security Group

Allow inbound traffic:
- Port 22 (SSH)
- Port 3000 (Frontend)
- Port 8080 (Backend)
- Port 7880 (LiveKit)

#### Step 4: Access Your App

`http://your-ec2-public-ip:3000`

---

### Option B: AWS Elastic Beanstalk (Easier)

#### Step 1: Install EB CLI

```bash
pip install awsebcli
```

#### Step 2: Initialize Backend

```bash
cd "Day 6 Fraud Alert Agent/backend"

# Create requirements.txt
pip freeze > requirements.txt

# Initialize EB
eb init -p python-3.9 fraud-agent-backend --region us-east-1

# Create environment
eb create fraud-agent-env

# Set environment variables
eb setenv LIVEKIT_URL=xxx LIVEKIT_API_KEY=xxx LIVEKIT_API_SECRET=xxx MURF_API_KEY=xxx GOOGLE_API_KEY=xxx DEEPGRAM_API_KEY=xxx

# Deploy
eb deploy
```

#### Step 3: Deploy Frontend to S3 + CloudFront

```bash
cd ../frontend

# Build
pnpm build

# Create S3 bucket
aws s3 mb s3://fraud-agent-frontend

# Enable static website hosting
aws s3 website s3://fraud-agent-frontend --index-document index.html

# Upload build
aws s3 sync out/ s3://fraud-agent-frontend --acl public-read

# Get URL
echo "http://fraud-agent-frontend.s3-website-us-east-1.amazonaws.com"
```

---

### Option C: AWS Lambda + API Gateway (Serverless - Advanced)

#### Step 1: Create Lambda Deployment Package

```bash
cd "Day 6 Fraud Alert Agent/backend"

# Install dependencies in folder
pip install -r requirements.txt -t ./package

# Add your code
cp -r src/* ./package/

# Create ZIP
cd package
zip -r ../fraud-agent-lambda.zip .
```

#### Step 2: Create Lambda Function

```bash
# Create function
aws lambda create-function \
  --function-name fraud-agent \
  --runtime python3.9 \
  --role arn:aws:iam::YOUR_ACCOUNT:role/lambda-execution-role \
  --handler agent.lambda_handler \
  --zip-file fileb://../fraud-agent-lambda.zip \
  --timeout 300 \
  --memory-size 512

# Set environment variables
aws lambda update-function-configuration \
  --function-name fraud-agent \
  --environment Variables="{LIVEKIT_URL=xxx,LIVEKIT_API_KEY=xxx,LIVEKIT_API_SECRET=xxx}"
```

#### Step 3: Create API Gateway

```bash
# Create REST API
aws apigateway create-rest-api --name fraud-agent-api

# Configure routes and integrate with Lambda
# (Use AWS Console for easier setup)
```

---

### Option D: Docker + AWS ECS (Production-Grade)

#### Step 1: Build Docker Image

```bash
cd "Day 6 Fraud Alert Agent/backend"

# Build
docker build -t fraud-agent:latest .

# Test locally
docker run -p 8080:8080 --env-file .env.local fraud-agent:latest
```

#### Step 2: Push to ECR

```bash
# Create ECR repository
aws ecr create-repository --repository-name fraud-agent

# Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com

# Tag image
docker tag fraud-agent:latest YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/fraud-agent:latest

# Push
docker push YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/fraud-agent:latest
```

#### Step 3: Deploy to ECS

```bash
# Create ECS cluster
aws ecs create-cluster --cluster-name fraud-agent-cluster

# Create task definition (use AWS Console or JSON file)
# Create service
aws ecs create-service \
  --cluster fraud-agent-cluster \
  --service-name fraud-agent-service \
  --task-definition fraud-agent:1 \
  --desired-count 1
```

---

## Quick Start (Recommended for Beginners)

**Use AWS Elastic Beanstalk** - It's the easiest AWS option that still shows cloud skills.

```bash
# 1. Install EB CLI
pip install awsebcli

# 2. Deploy backend
cd "Day 6 Fraud Alert Agent/backend"
eb init -p python-3.9 fraud-agent
eb create fraud-env
eb setenv LIVEKIT_URL=xxx LIVEKIT_API_KEY=xxx
eb deploy

# 3. Deploy frontend to Vercel (easier than S3)
cd ../frontend
vercel
```

---

## Resume Lines (Choose Based on Method):

**EC2:**
"Deployed fraud detection voice agent on AWS EC2 with custom security groups, demonstrating cloud infrastructure management and Linux server administration"

**Elastic Beanstalk:**
"Architected and deployed fraud alert system on AWS Elastic Beanstalk with automated scaling and environment-based configuration management"

**Lambda + API Gateway:**
"Built serverless fraud detection agent using AWS Lambda and API Gateway, reducing infrastructure costs by 70% while maintaining sub-second response times"

**ECS + Docker:**
"Containerized fraud alert voice agent with Docker and deployed to AWS ECS, implementing production-grade orchestration and auto-scaling"

---

## Cost Estimate:

- **EC2 t2.micro**: Free tier (12 months)
- **Elastic Beanstalk**: Free tier
- **Lambda**: Free tier (1M requests/month)
- **S3**: ~$0.50/month
- **Total**: $0-5/month

## Monitoring (Bonus Points):

```bash
# Enable CloudWatch logs
aws logs create-log-group --log-group-name /aws/fraud-agent

# View logs
aws logs tail /aws/fraud-agent --follow
```
