#!/bin/bash

export MIX_ENV=prod
export PORT=4999

echo "Beginning deploy of Teetime Bot..."

mix deps.get --only prod
mix compile

mix ecto.reset

(cd assets && npm install --prefix)
(cd assets && npm run deploy --prefix)
mix phx.digest
mix release

echo "Deploy successful..."
echo "Run start.sh to start your app"
