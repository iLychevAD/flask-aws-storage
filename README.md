### Prerequisites:
`aws` cli tool installed and configured.

CloudFormation (CFN further) nested Stacks feature requires a S3 bucket created beforehand CFN operatins.

### Description:

The app is just a primitive Flask based files-to-S3 uploader (also shows the pictures if any amongs files in S3, use `/pics` endpoint).

You deploy the solution using `main.cfn.yaml`.

It contains three nested CFN Stacks. 

The first one takes the specified Git repo and builds a Docker image from a Dockerfile within. Note, that only public repos are supported. Upon Stack update you need to pass a new value of the CFN `DockerImageTag` parameter to trigger building a new Docker image. An image is saved to an ECR registry.

The second nested CFN template creates a new VPC with isolated subnets (no routes to NAT gateways) to host a ECS with the app.

Finally, the last one creates a S3 bucket and spin ups an ECS cluster to run a task with the app.


### Deploy the solution:

`cd` to the `cfn` directory.

1. Package CFN templates (required because nested Stacks used):

`aws cloudformation package \`

`    --template-file main.cfn.yaml \`

`    --s3-bucket <pre-created S3 bucket for storing CFN templates> \`

`    --output-template-file packaged.cfn.yaml`

2. Kick off a CFN Stack creation:

`aws cloudformation create-stack --stack-name <any name> --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND --template-body file://packaged.cfn.yaml --parameters ParameterKey=DockerImageTag,ParameterValue=<e.g. Git commit sha> ParameterKey=GitRepoUrl,ParameterValue="https://github.com/<your name>/<repo name>.git" ParameterKey=EcrRepositoryName,ParameterValue=uploader`

For the `GitRepoUrl` specify the URL (as it consumed by `git clone`) of a Git repo containing a Dockerfile (i.e. the URL of this repo). CodeBuild project performs `git clone` of this URL to obtain a Dockerfile. Keep in mind, that public repos only supported.

 For the `DockerImageTag` specify some uniq value, i.e. a current date or Git commit sha. Note, that upon CFN Stack update the Docker build step is only triggered 
if the passed value of `DockerImageTag` differs from the one passed in to the previous CFN Stack operation (create or update).

If you need to update an already created CFN Stack, use `update-stack` instead of `create-stack`)


3. Navigate to the AWS web console to the CloudFormation Stacks section and enjoy watching the process of the Stack bootstraping.

The link to the LoadBalancer URL can be found in the `Outputs` tab of the AWS CloudFormation console..

### Cleanup
Select the Stack in the AWS web console and press the "Delete" button. 

Of course, it's also possible to delete a Stack using aws cli but Im too lazy to put here another several words about that way :-)

Note, that the solution contains CFN Custom Resource that would delete all of the images in the ECR and the content of the uploads S3 bucket upon deleting the Stack!

### Tips

`Ecs Exec` feature is configured for the ECS task in the solution. See https://aws.amazon.com/blogs/containers/new-using-amazon-ecs-exec-access-your-containers-fargate-ec2/.
