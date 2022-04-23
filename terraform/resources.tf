data "aws_ami" "ubuntu-linux-2004" {
  most_recent = true
  owners      = ["099720109477"]

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

resource "aws_instance" "smplverse_instance" {
  ami           = data.aws_ami.ubuntu-linux-2004.id
  instance_type = "t2.medium"
  count         = 1
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
    to_port     = 8000
  }
}

resource "aws_key_pair" "smplverse_key" {
  key_name   = "smplverse_key"
  public_key = file("~/.ssh/smplverse.pub")
}
