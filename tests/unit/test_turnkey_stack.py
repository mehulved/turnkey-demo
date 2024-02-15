import aws_cdk as core
import aws_cdk.assertions as assertions

from turnkey.turnkey_stack import TurnkeyStack

# example tests. To run these tests, uncomment this file along with the example
# resource in turnkey/turnkey_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = TurnkeyStack(app, "turnkey")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
