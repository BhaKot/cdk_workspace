from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_lambda as _lambda,
    aws_iam as _iam,
    aws_sqs as _sqs,
    custom_resources as cr,
)
from aws_cdk.aws_lambda_event_sources import SqsEventSource
import logging


class AwsHelpersStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        logging.info(f"Initializing AwsHelpersStack with ID: {construct_id}")

        # Create an SQS queue
        fifo_dlq = _sqs.Queue(
            self,
            "gar_qa_sf_infra_consumer_dlq_fifo",
            queue_name="gar_qa_sf_infra_consumer_dlq.fifo",
            fifo=True,
            visibility_timeout=Duration.seconds(
                300
            ),  # Should be greater than or equal to Lambda timeout
        )

        # Create an SQS queue
        fifo_queue = _sqs.Queue(
            self,
            "gar_qa_sf_infra_consumer_fifo",
            queue_name="gar_qa_sf_infra_consumer.fifo",
            fifo=True,
            content_based_deduplication=True,
            dead_letter_queue=_sqs.DeadLetterQueue(max_receive_count=3, queue=fifo_dlq),
            visibility_timeout=Duration.seconds(
                300
            ),  # Should be greater than or equal to Lambda timeout
        )

        # Create an IRole object from the existing role ARN
        lambda_role = _iam.Role.from_role_arn(
            self,
            "gar_lambda_role",
            role_arn="arn:aws:iam::527571104735:role/service-role/GAR_QA_SF_INFRA_LAMBDA-role-jfg7b4jv",
        )

        # Defines the AWS Lambda resource (for v2)
        gar_qa_sf_infra_lambda_v2 = _lambda.Function(
            self,
            "gar_qa_sf_infra_consumer_v2",
            runtime=_lambda.Runtime.PYTHON_3_12,
            code=_lambda.Code.from_asset("assets"),
            handler="lambda_function.lambda_handler",
            function_name="gar_qa_sf_infra_consumer_v2",
            role=lambda_role,
            description="My infra consumer lambda v2",
        )

        logging.info(
            f"Lambda function created/updated: {gar_qa_sf_infra_lambda_v2.function_name}"
        )

        # Add SQS as an event source for the Lambda
        gar_qa_sf_infra_lambda_v2.add_event_source(
            SqsEventSource(fifo_queue, batch_size=1)
        )

        logging.info(
            f"SQS queue : {fifo_queue.queue_name} created and set as trigger for Lambda v2"
        )

        logging.info("AwsHelpersStack initialization complete")
