#!/bin/bash

if [ $# -eq 0 ]; then
    echo 'port is not specified'
    exit 1
else
    PORT=$1
fi

pip install jupyterlab
jupyter notebook --generate-config

CONFIG=$(jupyter --config-dir)/jupyter_notebook_config.py

echo "c.NotebookApp.ip = '0.0.0.0'" >> $CONFIG
echo "c.NotebookApp.port = $PORT" >> $CONFIG
echo "c.NotebookApp.allow_origin = '*'" >> $CONFIG
echo "c.NotebookApp.allow_root = True" >> $CONFIG
echo "c.NotebookApp.allow_remote_access = True" >> $CONFIG
echo "c.NotebookApp.token = ''" >> $CONFIG
echo "c.NotebookApp.open_browser = False" >> $CONFIG

echo "Running jupyter server on port: $PORT"
jupyter notebook