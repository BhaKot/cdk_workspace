#!/usr/bin/env python3
import aws_cdk as cdk
from assets.aws_helpers_stack import AwsHelpersStack

app = cdk.App()
AwsHelpersStack(app, "AwsHelpersStack")
app.synth()
