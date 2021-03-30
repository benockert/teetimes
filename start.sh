#!/bin/bash

export MIX_ENV=prod
export PORT=4999

_build/prod/rel/teetimes/bin/teetimes start
