#!/bin/bash
#
# Wipes out the cloudformation stack
# Will not exit until delete is complete
#

aws cloudformation delete-stack --stack-name monkeyStack
aws cloudformation wait stack-delete-complete --stack-name monkeyStack
