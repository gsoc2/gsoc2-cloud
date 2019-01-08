import argparse

from .build import BuildCommand
from .upload_azure import UploadAzureCommand
from .upload_ec2 import UploadEc2Command
from .upload_gce import UploadGceCommand


parser = argparse.ArgumentParser(prog='debian-cloud-images')
subparsers = parser.add_subparsers(help='sub-command help')

BuildCommand._argparse_init_sub(subparsers)
UploadAzureCommand._argparse_init_sub(subparsers)
UploadEc2Command._argparse_init_sub(subparsers)
UploadGceCommand._argparse_init_sub(subparsers)


def main():
    args = parser.parse_args()
    args.cls(**vars(args))()