#!/usr/bin/env python3
import os
import aws_cdk as cdk
from infra.infra_stack import InfraStack

app = cdk.App()
env_account = os.environ.get("AWS_ACCOUNT_ID")
env_region = os.environ.get("AWS_REGION")

InfraStack(
    app,
    "OpenWeatherInfraStack",
    env=cdk.Environment(account=env_account, region=env_region),
)

app.synth()
