# Cameras record under Robonomics parachain control
## This repo is an exaple of using Raspberry Pi with ip cameras to demonstrate Robonomics application for various tasks
### Record or stream from several ip cameras using Robonomics tools

**Hardware**
- Raspberry Pi (4 tested fine)
- Number of IP cameras ([these](https://www.hikvision.com/europe/products/IP-Products/Network-Cameras/Pro-Series-EasyIP-/DS-2CD2125G0-IMS/?q=ds-2cd2125g0-ims&position=1) were used + power supply)
- Router

**Requirenments**

*This is to be installed on Raspberry Pi, connection to RPi may be established by [yggdrasil](https://yggdrasil-network.github.io/) + [ssh](https://phoenixnap.com/kb/ssh-to-connect-to-remote-server-linux-or-windows)*
- [Python 3](https://docs.python-guide.org/starting/install3/linux/) 
- `pip3 install pinatapy-vourhey`
- Robonomics node (binary file) (download latest release [here](https://github.com/airalab/robonomics/releases). Be careful to download arm architecture binary)
- ffmpeg (`sudo apt install ffmpeg`)
- account on [pinata](https://pinata.cloud/)

## To run:
1) Specify all the information in config file.

2) Manage accounts in DAPP (don't forget to save private raw and public keys):

2.1) Create a local robonomics network node with robonomics binary file:
```
./robonomics --dev --rpc-cors all
```
**Important!** Before next launches it is necessary to remove a directory `db` with
```
rm -rf /home/$USER/.local/share/robonomics/chains/dev/db
```

**OR**
2.2) You can specify `remote` field in config file to connect to remote node

**OR**
2.3) You can build an ssh port to test network with `ssh -L 9944:localhost:9944 <address>`

After a successful launch go to https://parachain.robonomics.network and switch to local node or remote one:

Go to Accounts and create **CAMERAS** (as much as needed) and **CONTROL** accounts. **Important**! Copy each account's raw key (change mnemonic seed to raw key while creating account) and address (to copy address click on account's icon) and add these addresses, keys and path to robonomics binary file to config. Transfer some money (units) to these accounts.

3) Launch program
```
python3 main.py
```

4) Now you can send a transaction triggering the camera to start recording. To do so, you should use the Robonomics IO `write` subcommand of robonomics binary file:
```
echo "ON" | ./robonomics io write launch -r <CAMERA_ADDRESS> -s <CONTROL’S_KEY>
```
Where `<CAMERA_ADDRESS>`  and `<CONTROL’S_KEY>` are replaced with  previously saved strings accordingly. Cameras work independently.

5) To stop recording
```
echo "OFF" | ./robonomics io write launch -r <CAMERA_ADDRESS> -s <CONTROL’S_KEY>
```
6)
IPFS hash of video will be available on robonomics platform  Chainstate->datalog->CAMERA
