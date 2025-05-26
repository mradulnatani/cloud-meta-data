sudo apt-get update
sudo apt install python3
sudo apt install python3-pip
sudo apt install python3-venv
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
cd cloud-meta-data
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
aws configure



