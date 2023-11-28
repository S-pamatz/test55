#!/bin/bash

./deployment/package.sh

read -p "Enter the <user> name: " user_name



source_directory="./package"
destination_server="172.232.172.160"
destination_directory="/test"

echo "Performing rsync."
rsync -av --checksum "${source_directory}"/* "${user_name}@${destination_server}:${destination_directory}/"

# Check if the SCP operation was successful
if [ $? -eq 0 ]; then
    echo "SCP completed successfully."
else
    echo "SCP encountered an error. Check your inputs and try again."
fi

rm -rf package

echo "Restarting the flask app"
ssh "${user_name}@${destination_server}" 'shared_pm2 restart my-flask'
