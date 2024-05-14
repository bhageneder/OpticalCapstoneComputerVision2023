#!/bin/bash

/bin/udevadm info --name=/ttyUSB$1 | grep ID_SERIAL=
