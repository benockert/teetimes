#!/bin/bash

export MIX_ENV=prod
export PORT=4999
export NODEBIN=`pwd`/assets/node_modules/.bin
export PATH="$PATH:$NODEBIN"

echo "Beginning deploy of Teetime Bot..."

mix deps.get
mix compile

(cd assets && npm install && webpack --node production)
mix phx.digest
mix release

echo "Deploy successful..."
echo "Run start.sh to start your app"
