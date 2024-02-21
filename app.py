#!/usr/bin/env python3
import os

import aws_cdk as cdk

from turnkey.turnkey_stack import TurnkeyStack

app = cdk.App()
branch = app.node.try_get_context("branch")
if branch:
    TurnkeyStack(app, f"TurnkeyStack-{branch}",
                 env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),

                 # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
                 )
else:
    TurnkeyStack(app, f"TurnkeyStack-dev",
                 env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),

                 # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
                 )
app.synth()
