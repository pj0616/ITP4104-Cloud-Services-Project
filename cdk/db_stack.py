from aws_cdk import (
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_cloudformation as cloudformation,
    aws_s3 as s3,
    aws_cloud9 as cloud9,
    aws_rds as rds,
    core
    )


class DBStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        # Exercise 9
        db_password_parameters = core.CfnParameter(self, "DBPassword",
            no_echo = True,
            description = "New account and RDS password",
            min_length = 1,
            max_length = 41,
            constraint_description = "the password must be between 1 and 41 characters",
            default = "DBPassword"
        )

        # DBSecurityGroup:
        db_security_group = ec2.CfnSecurityGroup(self, "DBSecurityGroup",
            group_description = "DB traffic",
            vpc_id = core.Fn.import_value("VPC"),
            security_group_ingress = [
            {
              "ipProtocol" : "tcp",
              "fromPort" : 3306,
              "toPort" : 3306,
              "sourceSecurityGroupId" : core.Fn.import_value("WebSecurityGroupOutput"),
            },
            {
              "ipProtocol" : "tcp",
              "fromPort" : 3306,
              "toPort" : 3306,
              "sourceSecurityGroupId" : core.Fn.import_value("EdxProjectCloud9Sg"),
            },
            {
              "ipProtocol" : "tcp",
              "fromPort" : 3306,
              "toPort" : 3306,
              "sourceSecurityGroupId" : core.Fn.import_value("LambdaSecurityGroupOutput"),
            }
            ],
            security_group_egress = [
            {
              "ipProtocol" : "tcp",
              "fromPort" : 0,
              "toPort" : 65535,
              "cidrIp" : "0.0.0.0/0"
            }
            ],
        )
        
        # MyDBSubnetGroup
        my_db_subnet_group = rds.CfnDBSubnetGroup(self, "DBSubnetGroup",
            db_subnet_group_description = "MyDBSubnetGroup",
            subnet_ids = [
                    core.Fn.import_value("PrivateSubnet1"),
                    core.Fn.import_value("PrivateSubnet2")
            ]
        )
        
        # RDSCluster
        rds_cluster = rds.CfnDBCluster(self, "RDSCluster",
            db_cluster_identifier = "edx-photos-db",
            database_name = "Photos",
            master_username = "master",
            master_user_password = db_password_parameters.value_as_string,
            engine_mode = "serverless",
            scaling_configuration = {
                "autoPause" : True,
                "maxCapacity" : 4,
                "minCapacity" : 2
            } ,
            engine = "aurora",
            db_subnet_group_name = my_db_subnet_group.ref,
            vpc_security_group_ids = [
                db_security_group.ref
            ]
        )
        rds_cluster.apply_removal_policy(core.RemovalPolicy.DESTROY)
        
        # Output
        core.CfnOutput(self, "MyDBEndpoint",
            value = rds_cluster.attr_endpoint_address,
            description = "MyDB Endpoint",
            export_name = "MyDBEndpoint"
        )