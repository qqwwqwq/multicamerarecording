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
*run main.py.*.   
*"r" on the keyboard for record, "s" on the keyboard for record for save*.   
**4.Replay**.  
*change the path of video for replay*
```
filename: str = "/mnt/storage/buildwin/multicameradata/A5-(22-07-2022-20-26-06)__c1.MKV"
```
*run replays.py*

## For Windows
**1.[Install the Azure Kinect SDK](https://github.com/microsoft/Azure-Kinect-Sensor-SDK/blob/develop/docs/usage.md)**

**2.Config the environment variables** 
Add the pyk4a.dll directory to the "Path". (Default is "C:\Program Files\Azure Kinect SDK v1.4.1\sdk\windows-desktop\AMD64\release\bin")

**3.Installation via Conda** 
*Preparing conda env: (Assuming you have conda installed)*
```
# We require python>=3.6
conda create -n multicamera python=3.6
conda activate multicamera
```
*Install requirements*
```
pip3 install opencv-contrib-python
pip install pyk4a --no-use-pep517 --global-option=build_ext --global-option="-IC:\Program Files\Azure Kinect SDK v1.4.1\sdk\include" --global-option="-LC:\Program Files\Azure Kinect SDK v1.4.1\sdk\windows-desktop\amd64\release\lib" #The path can be replaced according to your installation of Azune Kinect SDK
```

**4.Record and save**  
*run main.py.*.   
*"r" on the keyboard for record, "s" on the keyboard for record for save*.   

**5.Replay**.  
*change the path of video for replay*
```
filename: str = "D:/multicameradata/A5-(22-07-2022-20-26-06)__c1.MKV"
```
*run replays.py*
