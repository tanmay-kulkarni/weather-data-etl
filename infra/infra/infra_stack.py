from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
    CfnOutput,
    RemovalPolicy,
)

from pathlib import Path

# from constructs import Construct
from aws_cdk.aws_ec2 import (
    Instance,
    InstanceType,
    SecurityGroup,
    Port,
    Peer,
    KeyPair,
    SubnetType,
    Vpc,
)
from aws_cdk.aws_ec2 import AmazonLinuxImage, UserData, AmazonLinuxGeneration
from aws_cdk.aws_ec2 import InstanceClass  # Import the missing InstanceClass
from aws_cdk.aws_ec2 import InstanceSize  # Import the missing InstanceSize
from constructs import Construct


class InfraStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        key_pair = KeyPair.from_key_pair_name(
            self, "KeyPair", "ec2-portfolio-account-keypair"
        )

        # IF you want to use the default VPC, use the following code
        vpc = Vpc.from_lookup(
            self, "default_vpc", is_default=True, vpc_id="vpc-0ff3b0930968a7bfa"
        )

        # Create a Security Group
        security_group = SecurityGroup(
            self,
            "MySecurityGroup",
            vpc=vpc,
            description="Allow SSH access",
            allow_all_outbound=True,
        )

        security_group.add_ingress_rule(
            peer=Peer.ipv4("103.132.172.39/32"), connection=Port.tcp(22)
        )

        user_data = Path("infra/user_data_script.sh").read_text()

        # Create an EC2 Instance
        instance = Instance(
            self,
            "MyInstance",
            instance_type=InstanceType.of(
                InstanceClass.BURSTABLE2, InstanceSize.LARGE
            ),
            machine_image=AmazonLinuxImage(
                generation=AmazonLinuxGeneration.AMAZON_LINUX_2023
            ),
            vpc=vpc,
            security_group=security_group,
            key_pair=key_pair,
            user_data=UserData.custom(user_data),
        )

        # Output the public DNS of the instance
        CfnOutput(
            self, "InstancePublicDnsName", value=instance.instance_public_dns_name
        )
