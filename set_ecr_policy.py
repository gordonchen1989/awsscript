import boto3

client = boto3.client('ecr')

policyText = '''{
  "Version": "2008-10-17",
  "Statement": [
    {
      "Sid": "AllowPushPull",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::597931337143:root"
      },
      "Action": [
        "ecr:BatchCheckLayerAvailability",
        "ecr:BatchGetImage",
        "ecr:CompleteLayerUpload",
        "ecr:GetDownloadUrlForLayer",
        "ecr:InitiateLayerUpload",
        "ecr:PutImage",
        "ecr:UploadLayerPart"
      ]
    }
  ]
}'''

response = client.describe_repositories()

repo_list = response['repositories']

for repo in repo_list:
    registryId = repo['registryId']
    repositoryName = repo['repositoryName']
    print(f'id: {registryId},repoName: {repositoryName}')
    set_policy_response = client.set_repository_policy(
        registryId = registryId,
        repositoryName = repositoryName,
        policyText = policyText
    )
    print(f'{registryId},{repositoryName},response: {set_policy_response}')


