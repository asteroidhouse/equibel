#!/bin/bash

DIR=$1
FILES=`ls $DIR/*.py`
for file in $FILES
do
  sed 's/     /    /g' $file > $DIR/temp_file.py
  mv $DIR/temp_file.py $file
  echo "Fixed $file..."
done

echo
echo "Finished with directory ${DIR}."
