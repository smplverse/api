resource "aws_instance" "smplverse_instance" {
  ami           = var.PACKER_AMI
  instance_type = "g4dn.xlarge"
  key_name      = "smplverse_key"
  depends_on = [
    aws_security_group.smplverse_security_group
  ]
  vpc_security_group_ids = [
    aws_security_group.smplverse_security_group.id
  ]

  connection {
    type        = "ssh"
    user        = "ubuntu"
    private_key = file("~/.ssh/smplverse")
    timeout     = "4m"
    host        = self.public_ip
    password    = var.SSH_PASSWORD
  }
}

resource "aws_security_group" "smplverse_security_group" {
  egress {
    cidr_blocks = ["0.0.0.0/0"]
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
  }

  ingress {
    cidr_blocks = ["0.0.0.0/0"]
    protocol    = "tcp"
    from_port   = 22
    to_port     = 22
  }

  ingress {
    cidr_blocks = ["0.0.0.0/0"]
    protocol    = "tcp"
    from_port   = 80
    to_port     = 80
  }

  ingress {
    cidr_blocks = ["0.0.0.0/0"]
    protocol    = "tcp"
    from_port   = 443
    to_port     = 443
  }
}

resource "aws_key_pair" "smplverse_key" {
  key_name   = "smplverse_key"
  public_key = file("~/.ssh/smplverse.pub")
}

resource "aws_eip_association" "eip_assoc" {
  instance_id   = aws_instance.smplverse_instance.id
  allocation_id = var.ALLOCATION_ID
}
