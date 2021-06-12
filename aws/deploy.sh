#!/bin/bash
####################################################################
## Creates all necessary files for the deployment and deploys     ##
## them directly to AWS using terraform.                          ##
##                                                                ##
## It also supports the creation of a typeMappings.json.          ##
####################################################################


helpmenu () {
   echo -e "Usage: $0 [--help] [--region region] [--url] [--mapping]\n" 

   echo -e "Commands:"
   echo -e "\t--help\t\t\tShow this help output."
   echo -e "\t--region region\t\tSets a specific region for the deployment. Use a region from:"
   echo -e "\t\t\t\thttps://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.RegionsAndAvailabilityZones.html"
   echo -e "\t--url\t\t\tPrints out all deployment urls"
   echo -e "\t--mappings\t\tCreates typeMapping.json with the deployment urls"
}

showURL () {
   terraform show | tail -n 5
}

createMappings () {
   python3 createTypeMappings.py
}


region="us-east-1"

while [ ! $# -eq 0 ]
do
	case "$1" in
		--help | -h)
			helpmenu
			exit
			;;
        --url | -u)
			showURL
			exit
			;;
        --mappings | -m)
			createMappings
			exit
			;;
		--region)
            if [ -n "$2" ]; then
			    region=$2
			    shift
            else
                helpmenu
                exit
            fi
			;;
	esac
	shift
done

mkdir -p tmp
rm tmp/*.zip

./build.sh ../functions/sentim-batch
./build.sh ../functions/sentim-inference
./build.sh ../functions/sentim-inference-textblob
./build.sh ../functions/sentim-preprocess
./build.sh ../functions/sentim-reduce

terraform init

terraform apply -auto-approve -var="region=$region"

rm tmp/*.zip