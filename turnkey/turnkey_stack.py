from aws_cdk import (
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    Stack,
    # aws_sqs as sqs,
)
from constructs import Construct

class TurnkeyStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc(self, "DevVpc", max_azs=2)  # default is all AZs in region

        cluster = ecs.Cluster(self, "devCluster", vpc=vpc)

        ecs_patterns.ApplicationLoadBalancedFargateService(self, "DevApp",
                                                           cluster=cluster,  # Required
                                                           cpu=256,  # Default is 256
                                                           runtime_platform=ecs.RuntimePlatform(
                                                                operating_system_family=ecs.OperatingSystemFamily.LINUX,
                                                                cpu_architecture=ecs.CpuArchitecture.X86_64
                                                            ),
                                                           desired_count=2,  # Default is 1
                                                           task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                                                               image=ecs.ContainerImage.from_registry(
                                                                   "amazon/amazon-ecs-sample")),
                                                           memory_limit_mib=512,  # Default is 512
                                                           public_load_balancer=True)  # Default is True
