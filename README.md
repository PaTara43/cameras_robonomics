# Cameras for Transparent Production Under Robonomics Parachain Control

## This repository is an example of using Robonomics tools with single-board computer, IP camera and label printer to demonstrate providing trustworthy production surveillance

### Record video, store it in IPFS and send hash to blockchain. Optionally print sticky label with qr-code link to pinned video

Option for sending transactions - [this repo](https://github.com/PaTara43/robonomics_transaction_by_button_rpi4) ('panda' branch for this case).

**Used hardware**
- [LattePanda](https://www.lattepanda.com/products/2.html) 2/32 GB with **Ubuntu 18.04** installed;
- IP camera Hikvision HiWatch DS-I200C + power supply/PoE injector;
- Label printer [Xprinter XP-420B](https://www.xprintertech.com/xp-420b);
- _Optional_: Wi-Fi router [Mikrotik RB941-2nD](https://mikrotik.com/product/RB941-2nD) for scalability (e.g. add more cameras), remote access or stable Wi-Fi connection;
- _Optional_: Button to send transactions. Generally, GPIO may be used with other hardware.

**Used services**
- [Pinata](https://pinata.cloud/) as a pinning service to widely spread video over IPFS;
- [YOURLS](https://yourls.org/) to print qr-codes with short predefined links.

**Used software.** *This is to be installed on LattePanda, connection to which may be established by [yggdrasil](https://yggdrasil-network.github.io/) + [ssh](https://phoenixnap.com/kb/ssh-to-connect-to-remote-server-linux-or-windows)*

- [Python 3](https://docs.python-guide.org/starting/install3/linux/);
- Robonomics binary file (download latest release [here](https://github.com/airalab/robonomics/releases));
- [FFMPEG](https://ffmpeg.org)
```bash
sudo apt install ffmpeg
```
- [IPFS](https://ipfs.io/):
```bash
wget https://dist.ipfs.io/go-ipfs/v0.6.0/go-ipfs_v0.6.0_linux-arm.tar.gz
tar -xvf go-ipfs_v0.6.0_linux-arm.tar.gz
rm go-ipfs_v0.6.0_linux-amd64.tar.gz go-ipfs_v0.6.0_linux-arm.tar.gz
sudo ./go-ipfs/install.sh
rm -rf go-ipfs
```
- [CUPS](https://www.cups.org/):
```bash
sudo apt install cups python3-cups
```

## Preparations
1) Install Ubuntu 18.04 on LattePanda;
2) Install all the software;
4) Set up IP camera. It should have a static IP to put it in configuration file. HD quality is recommended for less file size. Feel free to adjust OSD info;
5) Set up YOURLS server;
6) Set up a printer. For this case, you need to download [drivers](https://www.xprintertech.com/for-linux) and install them;
7) Set up CUPS server and add your printer. Don't forget to add you username to cups configuration files to be able to manage your printer;
8) If you use a button, solder it to GPIO board and [set it up for transactions sending](https://github.com/PaTara43/robonomics_transaction_by_button_rpi4);
9) If you use router, set it up to connect camera to LattePanda and connect router to the internet;

## To run:
1) Download source code and install additional python libraries:
```bash
git clone https://github.com/PaTara43/cameras_robonomics
cd cameras_robonomics
pip install -r requirements.txt
```
2) Specify all the information in configuration file.
```bash
nano config/config.yaml
```
It has comments for better understanding. **Read them carefully.** All the information about creating accounts may be found [here](https://wiki.robonomics.network/docs/create-account-in-dapp/). To send transactions between accounts they should have some tokens.

3) Launch script
```
python3 main.py
```

4) Now you can send a transaction triggering the camera to start recording. To do so, you should use the Robonomics IO `write` subcommand of robonomics binary file:
```bash
echo "ON" | ./robonomics io write launch -r <CAMERA_ADDRESS> -s <CONTROL’S_KEY> --remote <remote ws>
```
```bash
echo "OFF" | ./robonomics io write launch -r <CAMERA_ADDRESS> -s <CONTROL’S_KEY> --remote <remote ws>
```
or you may use button.

## How it works
Once camera receives "ON" transaction, it creates a short URL redirecting to nowhere (IPFS gateway with no hash), creates a qr-code with this short URL, prints the qr and starts filming. Once "OFF" transaction is received, it stops filming, publishes video to IPFS, changes short URL redirection link to gateway with hash address of the video and sends the video to Pinata pinning service for wider spreading over IPFS. IPFS hash of the video will be available on Robonomics platform Chainstate->datalog->CAMERA and stored there securely.

## Auto-start
You may want to auto-restart this script. To be able so, edit service file
```bash
nano services/robonomics_cameras.service
```
and fill it with path to python3 and the script. Don't forget to fill in username. E.g.:
```
ExecStart=/usr/bin/python3 /home/ubuntu/cameras_robonomics/main.py
User=ubuntu
```
Then move it to `/etc/systemd/system/` and run:
```bash
sudo mv services/robonomics_cameras.service /etc/systemd/system/
systemctl enable robonomics_cameras
systemctl start robonomics_cameras
```
To check service status do:
```bash
systemctl -l status robonomics_cameras
```
