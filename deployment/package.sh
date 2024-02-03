#!/bin/bash
echo "Runing react build."
(
    cd visualization/frontend
    npm install
    npm run build
)

if [ -d "package" ]; then
    rm -r package
fi

echo "Copying static files from react generated code."
mkdir package
cp -r fullStack package
cp -r visualization/frontend/build/* package/fullStack/app/View/static
cp -r visualization/backend package/visBackend

echo "Transforming index.html to work with the flask app's file structure."
python ./deployment/react_to_flask.py visualization/frontend/build/index.html package/fullStack/app/View/templates/react_app.html