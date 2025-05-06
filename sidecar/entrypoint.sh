#!/bin/bash

LOG_FILE="/var/log/nfd.log"

# 起動前の初期化
nfd-stop
sleep 2
nfd-start > $LOG_FILE 2>&1 &
sleep 5

# NLSR 起動
if [ ! -f "$NLSR_CONFIG_FILE_PATH" ]; then
  echo "NLSR configuration file not found. NLSR_CONFIG_FILE_PATH=$NLSR_CONFIG_FILE_PATH"
  exit 1
fi
echo "Using NLSR configuration file: $NLSR_CONFIG_FILE_PATH"
nlsr -f "$NLSR_CONFIG_FILE_PATH" > /dev/null 2>&1 &
sleep 2

# Neighbor に接続
grep -A 3 "neighbor" "$NLSR_CONFIG_FILE_PATH" | while read -r line; do
  if echo "$line" | grep -q "face-uri "; then
    URI=$(echo "$line" | sed -n 's/.*face-uri \(.*\)/\1/p')
    echo "Creating face for $URI"
    nfdc face create "$URI" > /dev/null 2>&1 &
  fi
done

echo "All faces created."

PREFIX=${NDN_FUNCTION_PREFIX}
python3 main.py "$PREFIX"
