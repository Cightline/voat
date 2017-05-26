#!/bin/bash
# Installs voat with dependecies onto server.
# Requires Python3 and pip
# Run as root

if [ "$(id -u)" != "0" ]; then
  echo "This script must be run as root" 1>&2
  exit 1
fi

VOAT_DIR=/etc/voat
SRC_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "Creating Voat directories at $VOAT_DIR"
mkdir -pv $VOAT_DIR
mkdir -pv $VOAT_DIR/db
mkdir -pv $VOAT_DIR/config

echo
echo "Creating link to config $SRC_DIR/config/config.json -> $VOAT_DIR/config/config.json"
ln -svf $SRC_DIR/config/config.json $VOAT_DIR/config/config.json

echo
echo "Adding voat user and setting permissions for $VOAT_DIR"
useradd voat
chown -R voat:voat $VOAT_DIR
chmod -R 775 $VOAT_DIR
echo
echo "Checking for python3..."
PYTHON_VERSION=$(echo $(python3 -c 'import sys; print(sys.version_info[:])') | cut -d',' -f1 | sed -e "s/(//g")
if [ $PYTHON_VERSION = "3" ]; then
	echo "Found python3"
else
	echo "Could not find a compatible python version"
	exit 2
fi

#Install dependencies with pip
echo
echo "Checking for pip..."
pip --version
if [ $? != "0" ]; then
	echo "Could not find pip"
	exit 3
else
	pip install flask
	pip install flask-restful
	pip install flask-cors
	pip install sqlalchemy
	pip install passlib
	pip install voluptuous
	pip install pycrypto
	pip install sqlalchemy_utils
	pip install requests
	pip install celery
	pip install redis
fi

echo
echo "Configuring voat..."
cd $SRC_DIR/libs
python3 setup.py install
cd $SRC_DIR
python3 tools/create_db.py


echo
echo "Creating server management script at /usr/bin/voat"

cp -f bin/voat /usr/bin/voat
sed -i "s@src-dir@$SRC_DIR@" /usr/bin/voat
chmod +x /usr/bin/voat

voat restart
