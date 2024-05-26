#!/usr/bin/env python3

import aws_cdk as cdk

from cdk_workspace.cdk_workspace_stack import CdkWorkspaceStack


app = cdk.App()
CdkWorkspaceStack(app, "CdkWorkspaceStack")

app.synth()
