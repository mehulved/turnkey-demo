from aws_cdk import (
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_route53 as route53,
    aws_ecs_patterns as ecs_patterns,
    Stack,
    aws_ecr as ecr,
)
from constructs import Construct

class TurnkeyStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc(self, "DevVpc", max_azs=2)  # default is all AZs in region

        branch = self.node.try_get_context('branch')
        if branch:
            cluster_name = f"{branch}Cluster"
            domain_name = f"{branch}.dev.pouringcat.com"
            environment = {"turnkey": "true", "turnkey_name": f"{branch}"}
            app_name = f"{branch}App"
        else:
            cluster_name = "devCluster"
            domain_name = "dev.pouringcat.com"
            environment = {"turnkey": "false"}
            app_name = "DevApp"

        repository = ecr.Repository.from_repository_name(self, "TurnkeyNginx", "turnkey-nginx")
        container = ecs.ContainerImage.from_ecr_repository(repository, "green")

        cluster = ecs.Cluster(self, cluster_name, vpc=vpc)
        domain_zone = route53.HostedZone.from_lookup(self, "pouringcat", domain_name="pouringcat.com")

        ecs_patterns.ApplicationLoadBalancedFargateService(self, app_name,
                                                           cluster=cluster,  # Required
                                                           cpu=256,  # Default is 256
                                                           runtime_platform=ecs.RuntimePlatform(
                                                                operating_system_family=ecs.OperatingSystemFamily.LINUX,
                                                                cpu_architecture=ecs.CpuArchitecture.ARM64
                                                            ),
                                                           desired_count=2,  # Default is 1
                                                           task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                                                               image=container,
                                                               environment=environment),
                                                           memory_limit_mib=512,  # Default is 512
                                                           public_load_balancer=True,
                                                           domain_zone=domain_zone,
                                                           domain_name=domain_name)  # Default is True