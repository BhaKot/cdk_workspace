from constructs import Construct
from aws_cdk import Stack


class AwsHelpersStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
