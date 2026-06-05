import * as cdk from 'aws-cdk-lib/core';
import { Construct } from 'constructs';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as path from 'path';

export class InfraStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const dataLakeBucket = new s3.Bucket(this, 'SecureCommerceDataLake', {
      versioned: true,                                      
      encryption: s3.BucketEncryption.S3_MANAGED,           
      blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,     
      removalPolicy: cdk.RemovalPolicy.DESTROY,             
      autoDeleteObjects: true                               
    });

    const ingestionLambda = new lambda.Function(this, 'CommerceIngestionHandler', {
      runtime: lambda.Runtime.PYTHON_3_11,                  
      handler: 'ingest.lambda_handler',                   
      code: lambda.Code.fromAsset(path.join(__dirname, '../../src')), 
      timeout: cdk.Duration.seconds(30),                    
      environment: {
        BUCKET_NAME: dataLakeBucket.bucketName
      }
    });

    dataLakeBucket.grantWrite(ingestionLambda);

    new cdk.CfnOutput(this, 'DataLakeBucketName', {
      value: dataLakeBucket.bucketName,
      description: 'The physical name of our secure S3 Data Lake bucket',
    });
  }
}
