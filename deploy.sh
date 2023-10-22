#!/bin/bash

read -p "Enter the <user> name: " user_name

if [ -d "package" ]; then
    rm -r package
fi

# copying static file from react generated code.
mkdir package
cp -r fullStack package
cp -r visualization/frontend/build/* package/fullStack/app/View/static

# transforming index.html to work with the flask app's file structure.
python react_to_flask.py visualization/frontend/build/index.html package/fullStack/app/View/templates/react_app.html

source_directory="./package"
destination_server="172.232.172.160"
destination_directory="/test"

# Perform SCP to copy the contents of the source directory to the remote server
rsync -av --checksum "${source_directory}"/* "${user_name}@${destination_server}:${destination_directory}/"

# Check if the SCP operation was successful
if [ $? -eq 0 ]; then
    echo "SCP completed successfully."
else
    echo "SCP encountered an error. Check your inputs and try again."
fi

rm -rf package

# Restart the flask app using pm2 on the destination server
ssh "${user_name}@${destination_server}" 'pm2 restart my-flask'