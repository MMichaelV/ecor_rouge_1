npm install -g serverless
pip install --user virtualenv
git clone https://github.com/MMichaelV/ecor_rouge_1.git ecor_route
cd ecor_route
virtualenv venv
source ./venv/bin/activate
pip install awscli
aws configure # and configure credentials
aws s3api create-bucket --bucket ecor-rouge-work

# Serverless S3 File Handler
cd lambdas/s3handler
sls plugin install --name serverless-plugin-existing-s3
sls s3deploy # made trigger
sls deploy
