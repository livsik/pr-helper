#!/bin/bash

mkdir -p "~/bin"

FILE="~/bin/ticket.py"
if test -f "$FILE"; then
rm "$FILE"
fi

cp ticket.py ~/bin