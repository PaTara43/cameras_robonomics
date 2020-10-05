# Cameras record under Robonomics parachain control

### Record or stream from several ip cameras using Robonomics tools

- pip install -r requirements.txt
- Robonomics node (binary file) (download latest release [here](https://github.com/airalab/robonomics/releases))
- IPFS 0.4.22 (download from [here](https://dist.ipfs.io/go-ipfs/v0.4.22/go-ipfs_v0.4.22_linux-386.tar.gz) and install)

## To run:
1) Specify all the information in config file.

2) Manage accounts in DAPP, launch IPFS
Create a local robonomics network node with robonomics binary file:
```
./robonomics --dev
```
**Important!** Before next launches it is necessary to remove a directory `db` with
```
rm -rf /home/$USER/.local/share/robonomics/chains/dev/db
```
After a successful launch go to https://parachain.robonomics.network and switch to local node:

Go to Accounts and create **CAMERAS** (as much as needed) and **EMPLOYER** accounts. **Important**! Copy each account's raw key and address (to copy address click on account's icon) and add these addresses, keys and path to robonomics binary file to config. Transfer some money (units) to these accounts.

```
ipfs init #once
ipfs daemon
```
3)
```
python main.py
```

4) Now you can send a transaction triggering the camera to start recording. To do so, you should use the Robonomics IO `write` subcommand of robonomics binary file:
```
echo "ON" | ./robonomics io write launch -r <CAMERA_ADDRESS> -s <EMPLOYER’S_KEY>
```
Where `<CAMERA_ADDRESS>`  and `<EMPLOYER’S_KEY>` are replaced with  previously saved strings accordingly. Cameras work independently.

5) To stop recording
```
echo "OFF" | ./robonomics io write launch -r <CAMERA_ADDRESS> -s <EMPLOYER’S_KEY>
```
6)
IPFS hash of video will be available in Chainstate->datalog->CAMERA
