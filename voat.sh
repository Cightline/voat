#!/bin/bash
if [ "$(id -u)" != "0" ]; then
	echo "Voat must be run as root" 1>&2
	exit 1
fi
SRC_DIR="src-dir"

case "$1" in
	start)
		"Starting Voat server..."
		/usr/bin/python3 $SRC_DIR/rest_server.py
		echo $! > /var/run/voat.pid
		;;
	stop)
		if [ -f /var/run/voat.pid ]; then
			echo "Stopping Voat..."
			kill -9 $(cat /var/run/voat.pid)
			rm /var/run/voat.pid
			
		else
			echo "Voat is not running."
		fi
		;;
	restart)
		stop
		start
		;;
	*)
		echo "Usage: sudo voat start|stop|restart"
		exit 1
esac
