# Cameras record under Robonomics parachain control

### Record or stream from several ip cameras using Robonomics tools

- pip install -r requirements.txt
- Robonomics node (binary file) (download latest release [here](https://github.com/airalab/robonomics/releases))

## To run:
1) Specify all the information in config file.

2) Manage accounts in DAPP
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

3)
```
python main.py
```

4) Now you can send a transaction triggering the camera to start recording/streaming. To do so, you should use the Robonomics IO `write` subcommand of robonomics binary file:
```
echo "ON" | ./robonomics io write launch -r <CAMERA_ADDRESS> -s <EMPLOYER’S_KEY>
```
Where `<CAMERA_ADDRESS>`  and `<EMPLOYER’S_KEY>` are replaced with  previously saved strings accordingly. Cameras work independently.

5) To stop recording/streaming
```
echo "OFF" | ./robonomics io write launch -r <CAMERA_ADDRESS> -s <EMPLOYER’S_KEY>
```
