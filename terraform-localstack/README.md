# terraform-localstack/ — Infrastructure as Code (Terraform)

Provisions cloud infrastructure for the ML system — an **S3 bucket** for model
artifacts and a **DynamoDB table** for predictions — using Terraform against
**LocalStack**, a local AWS emulator. No AWS account or credentials required, so
you run a real `terraform apply` end to end.

## What this demonstrates
- Authoring Terraform: providers, resources, outputs, version constraints.
- The core IaC loop: `init` → `plan` → `apply` → `destroy`.
- Pointing a provider at a custom endpoint (LocalStack) — the same technique used
  to target different AWS accounts/regions.

## Run it
```bash
# 1. start LocalStack
docker compose up -d

# 2. provision
terraform init
terraform plan
terraform apply -auto-approve

# 3. verify the resources really exist in LocalStack
aws --endpoint-url=http://localhost:4566 s3 ls
aws --endpoint-url=http://localhost:4566 dynamodb list-tables --region us-east-1

# 4. tear down
terraform destroy -auto-approve
docker compose down
```

## Be able to explain (interview-ready)
- What `terraform init`, `plan`, and `apply` each do.
- Why state matters and what `terraform.tfstate` holds.
- The difference between `PAY_PER_REQUEST` and provisioned DynamoDB capacity.
- How the `endpoints` block retargets the provider (real AWS vs. LocalStack).
