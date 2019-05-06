# TJBot text to image generation demo
Demo video [here](https://youtu.be/sjgLyykEZqI)

### To run the design at TJBot side to interact with users
1. Download files in "client" repo folder and put in home folder of raspberry pi
2. Boot the TJBot
3. At home folder of pi, run command "bash run_tjbot.sh"

### To run the code at xcloud server for serving front-end TJbot
1. ssh ubuntu@xcloud3 (pw: ubuntu)
2. Set the environment by command "source activate tjbot"
3. At home folder of xcloud3, run command "sudo bash run_tjserver.sh"

### Note
1. All the server side design codes are at "tjbot" folder under home directory if you want to check details ("server" repo folder here extracts tjbot-serving codes but not GAN models which have big sizes)
2. The current text recognition is updated with Google vision OCR API, which is capable of recognizing even hand-written text in a photo, but has 1000 free requests/month limit. We can still switch to Watson OCR system which is not well supported currently.
3. When speaking commands to TJBot, speak slowly and closely to the microphone, better using "what do you see", "what are you looking at", etc, to be recognized easier by Watson speech recognition APIs


