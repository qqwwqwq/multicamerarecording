# multicamerarecording
## For linux
**1.Install the dependency library Pyk4a**
```
pip install Pyk4a
```
**2.change the video save path**
```
 record = PyK4ARecord(device=k4a, config=config, path="/mnt/storage/buildwin/multicameradata/"+ "A5" +dt_string+"__c1.MKV")
 record2 = PyK4ARecord(device=k4a2, config=config2, path="/mnt/storage/buildwin/multicameradata/"+ "A5" +dt_string+"__c2.MKV")
```
**3.Record and save**
*run main.py. "r" on the keyboard for record, "s" on the keyboard for record for save*
**4.Replay**
*change the path of video for replay*
```
filename: str = "/mnt/storage/buildwin/multicameradata/A5-(22-07-2022-20-26-06)__c1.MKV"
```
*run replays.py*
