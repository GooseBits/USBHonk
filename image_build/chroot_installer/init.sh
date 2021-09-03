#!/bin/bash -e

# Run from the directory of the script
cd $( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Run individual scripts
for script in ./scripts/*.sh
do
  . $script
done
