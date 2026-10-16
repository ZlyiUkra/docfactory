# Upstash Terraform Provider
# джерело: https://github.com/upstash/terraform-provider-upstash/blob/v1.4.0/README.md
# отримано: 2026-10-16
# версія: terraform-1.4.0, terraform-1.3.0, terraform-1.2.6, terraform-1.2.5, terraform-1.2.4, terraform-1.2.3, terraform-1.2.2, terraform-1.2.1, terraform-1.2.0, terraform-1.1.5, terraform-1.1.4, terraform-1.1.3, terraform-1.1.2, terraform-1.1.1, terraform-1.1.0, terraform-1.0.3, terraform-1.0.2, terraform-1.0.1, terraform-1.0.0

This is the repository of official Upstash Terraform provider.

## Installation

```hcl

terraform {
  required_providers {
    upstash = {
      source = "upstash/upstash"
      version = "x.x.x"
    }
  }
}

provider "upstash" {
  email = var.email
  api_key  = var.api_key
}
```

`email` is your registered email in Upstash.

`api_key` can be generated from Upstash Console. For more information please check our docs.

## Create Database Using Terraform

Here example code snippet that creates database:

```hcl
resource "upstash_database" "mydb" {
  database_name = "mydb3"
  region = "eu-west-1"
  tls = "true"
  multi_zone = "false"
}
```
You can check full spec and doc from here.

## Support, Bugs Reports, Feature Requests

If you need support then you can ask your questions Upstash Team in upstash.com chat widget.

There is also discord channel available for community. Please check here for more information.

## Requirements

* Terraform v0.13 and above
* Go 1.16 (to build the provider)

## Development

If you want to locally build/test the provider then follow these steps:

* Build the provider using: `go build .` command, it will create executable in same directory
* create `terraform.rc` file that contains following configuration.
* export `TF_CLI_CONFIG_FILE` env variable that locates `terraform.rc` file.
* Now your `terraform` commands will use local Upstash provider.
```hcl
provider_installation {

  dev_overrides {
    "upstash" = "[PATH THAT CONTAINS CUSTOM PROVIDER]"
  }
  direct {}
}
```
