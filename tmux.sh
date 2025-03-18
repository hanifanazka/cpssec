#!/sbin/bash

tmux new-session mosquitto \; new-window 'python mqtt_logger.py' \; new-window 'python device_simulator.py' \; new-window 'python dashboard.py'
