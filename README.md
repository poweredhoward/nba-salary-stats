Python 3.7
Postgres 12.7

What did I do for deployment?

https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-flask.html
https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-rds.html#python-rds-create

eb deploy to redeploy
eb ssh to ssh into maching
ssh'ed -> var/app/venv is virtual env
ran upgrade manually
.ini is pointing to RDS instance rn
Run seed function