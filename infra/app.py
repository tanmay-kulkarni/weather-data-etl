#!/usr/bin/env python3
import os
import aws_cdk as cdk
from infra.infra_stack import InfraStack

app = cdk.App()

InfraStack(
    app,
    "OpenWeatherInfraStack",
    env=cdk.Environment(account="", region="ap-south-1"),
)

app.synth()
