# . /home/ubuntu/torch/install/bin/torch-activate
export FLASK_APP=AttnGAN_server.py
export FLASK_DEBUG=1
python -m flask run --host 0.0.0.0 --port 3000
