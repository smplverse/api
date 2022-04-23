variable "REGION" {
  type    = string
  default = "us-east-2"
}

variable "AWS_ACCESS_KEY" {
  type      = string
  sensitive = true
}

variable "AWS_SECRET_KEY" {
  type      = string
  sensitive = true
}

variable "SSH_PASSWORD" {
  type      = string
  sensitive = true
}

variable "PACKER_AMI" {
  type      = string
  sensitive = false
  default   = "ami-0e7593b27916cb057"
}
