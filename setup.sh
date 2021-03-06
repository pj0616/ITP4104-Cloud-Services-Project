#!/bin/bash
echo -e "\033[36mInstall AWS CDK\033[0m"
npm install -g aws-cdk
echo -e "\033[36mCreate Python env\033[0m"
python3 -m venv .env
source .env/bin/activate
echo -e "\033[36mInstall requirements other_requirements.txt\033[0m"
pip install -r other_requirements.txt
echo -e "\033[36mInstall requirements requirements.txt\033[0m"
pip install -r requirements.txt
echo -e "\033[36mCDK synth\033[0m"
cdk synth
echo -e "\033[36mCDK deploy VpcStack IAMStack ParametesStack CognitoStack\033[0m"
cdk deploy VpcStack IAMStack ParametersStack CognitoStack
echo -e "\033[36mCDK deploy SecurityStack Cloud9Stack\033[0m"
cdk deploy SecurityStack Cloud9Stack 
echo -e "\033[36mCDK deploy CdnStack DBStack\033[0m"
cdk deploy CdnStack DBStack  
echo -e "\033[35mEND\033[0m"
