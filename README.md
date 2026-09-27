Hello everyone ! I have created this patch to revive the multiplayer mode (online) on the mobile game Wargunners: Online 2D Shooter !

> WARNING: I used AI to help develop this patch, given that I'm new to Android modding.

> [!NOTE] USEFUL INFORMATION

> It was published on the Google Play Store and available for download from August 20, 2018, to January 11, 2022, before being removed.

I opened the game's binaries using Ghidra—a program for reading and editing APK configuration files—and discovered that the game's servers were hosted on Photon Engine. However, the developer had deleted their account from the platform, effectively taking the servers offline. But rest assured: Photon Engine's servers are still up and running! That is why I developed these patches, so you can play the game again with your friends and family!

This game uses an AppID (server identifier) ​​to connect for multiplayer. I developed these patches so you can replace the defunct AppID with your own!
 
> [!NOTE] 1.HOW TO USE
 
 You need to open the downloaded game APK—not extract it—and select the file(s) appropriate for your device:
 
 for 64 bits devices: lib/arm64-v8a/libMyGame.so
 
 for 32 bits devices: lib/armabi-v7a/libMyGame.so
 
 If your device is 64-bit, take libMyGame.so from arm64-v8a
If your device is 32-bit, take libMyGame.so from armeabi-v7a
 
 Next, depending on the libMyGame.so file you just obtained (32-bit or 64-bit), rename it/them as follows:
 
 arm64-v8a(64 bits): libMyGame64.so
 armabi-v7a(32 bits): libMyGame32.so

> [!NOTE] 2.PATCHING

You must have Python installed, as well as zipalign and apksigner, to sign your APK; otherwise, you will not be able to install it. If you do not have them, run this command:

sudo apt install python3 zipalign apksigner

I have provided you with two Python files:

patch64 for libMyGame64.so
patch32 for libMyGame32.so

WARNING: Open the Python file and replace the Xs in "nouvel_app_id=" with your generated AppId. See here to create your AppId.

Next, run the file(s) you just modified. > WARNING: The file must be in the same directory as your libMyGame32/64.so!

for patch64: python3 patch64.py

for patch32: python3 patch32.py

If everything went well, the script should tell you: Patched file saved : libMyGame64_patched.so/libMyGame32_patched.so

> [!NOTE] 3.MAKE PATCHED APK

Replace the libMyGame.so files you extracted from the APK with your new, modified libMyGame64_patched.so/libMyGame32_patched.so files. Remember to rename them back to libMyGame.so

Once this is done, you need to align the APK—that is, optimize the application. Run this command:

zipalign -f -v 4 wargunners.apk wargunners_aligned.apk

Next, you need to sign the APK using apksigner. You need to generate a key. If you already have one, you can skip this step:

keytool -genkey -v \
  -keystore my_key.jks \
  -alias monalias \
  -keyalg RSA \
  -keysize 2048 \
  -validity 10000
  
  It will ask you for a password and some information (name, country, etc.) — enter whatever you like.
  
  Next, you can sign your APK: 
  
  apksigner sign \
  --ks my_key.jks \
  --ks-key-alias monalias \
  --out wargunners_patched.apk \
  wargunners_aligne.apk
  
  All that's left is to install your APK and share it with your friends!
