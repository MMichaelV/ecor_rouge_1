npm install -g serverless
pip install --user virtualenv
git clone https://github.com/MMichaelV/ecor_rouge_1.git ecor_route
cd ecor_route
virtualenv venv
source ./venv/bin/activate
pip install awscli
aws configure # configure credentials
# or run
# export AWS_DEFAULT_REGION=us-east-1 && export AWS_ACCESS_KEY_ID=<KEY_ID> && export AWS_SECRET_ACCESS_KEY=<ACCESS_KEY>
aws s3api create-bucket --bucket ecor-rouge-serverless-packages
aws s3api create-bucket --bucket ecor-rouge-work

# Serverless S3 File Handler
cd lambdas/s3handler
sls plugin install --name serverless-plugin-existing-s3
sls deploy
sls s3deploy # made trigger

# remove all data
sls s3eventremove
sls remove
aws s3api delete-bucket --bucket ecor-rouge-serverless-packages
aws s3api delete-bucket --bucket ecor-rouge-work

