#!/usr/bin/env python3
import os

import aws_cdk as cdk

from turnkey.turnkey_stack import TurnkeyStack


app = cdk.App()
TurnkeyStack(app, "TurnkeyStack",
    env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),

    # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
    )

app.synth()
