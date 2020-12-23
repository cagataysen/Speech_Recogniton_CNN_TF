import requests
import json
from predictNumbers import Predict_Number

import wave
import pyaudio
from scipy.io.wavfile import read
import trimAudio
from soundfile import SoundFile, SEEK_END
import numpy as np


"""
# server url
URL = "http://127.0.0.1:5000/predict"
TEST_URL = "https://olcer.net/capstone/API/notify"
headers = {
    "User-Agent": "PostmanRuntime/7.26.8", 
}
"""

# Constants for voice recording
RECORDED_AUDIO = "rawAudio.wav"
chunk = 1024
FORMAT = pyaudio.paInt16
channels = 1
sample_rate = 16000 
record_seconds = 2
p = pyaudio.PyAudio()

def recordVoice(FORMAT, channels, sample_rate, input, output, chunk):
    # 5 seconds voice recording
    stream = p.open(format=FORMAT,
                channels=channels,
                rate=sample_rate,
                input=True,
                output=True,
                frames_per_buffer=chunk)

    frames = []
    print("Recording...")
    for _ in range(int(sample_rate / chunk * record_seconds)):
        data = stream.read(chunk)
        # if you want to hear your voice while recording
        # stream.write(data)
        frames.append(data)
    print("Finished recording.")
    # stop and close stream
    stream.stop_stream()
    stream.close()
    # terminate pyaudio object

    # p.terminate() # Comment this line

    # save audio file
    # open the file in 'write bytes' mode
    wf = wave.open(RECORDED_AUDIO, "wb")
    # set the channels
    wf.setnchannels(channels)
    # set the sample format
    wf.setsampwidth(p.get_sample_size(FORMAT))
    # set the sample rate
    wf.setframerate(sample_rate)
    # write the frames as bytes
    wf.writeframes(b"".join(frames))
    # close the file
    wf.close()

def numberToInt(str):
    if str == "zero":
        return 0
    elif str == "one":
        return 1
    elif str == "two":
        return 2
    elif str == "three":
        return 3
    else:
        return 4

def isFan(device):
    if(device == 4):
        return True
    
    return False
    

def actionToInt(str):
    if str == "on":
        return 1
    else:
        return 0





if __name__ == "__main__":

    isContinue = True
    
    while isContinue :
        fullPhrase = ""
        print("#################\nFor LED 1: say 'one'\nFor LED 2: say 'two'\nFor LED 3: say 'three'\nFor Fan: say 'four'\n#################")
        # Get device number
        print("#################\nWhat is the number of the device that you want to interact with?\n#################")
        input("Press ENTER to record  your voice...")
        recordVoice(FORMAT, channels, sample_rate, True, True, chunk)
        trimAudio.trimAudio(1, 'rawAudio.wav')
        pn = Predict_Number()
        device = pn.predict('trimedAudio.wav')

        deviceNum = numberToInt(device)
        print(deviceNum)

        fullPhrase += device + " "
        print(fullPhrase)

        if(isFan(deviceNum)):
            print("#################\nTo adjust fan speed say numbers between 0 and 4:\n0 turns off the fan\n4 is the max speed\n#################")
            input("Press ENTER to record  your voice...")
            recordVoice(FORMAT, channels, sample_rate, True, True, chunk)
            trimAudio.trimAudio(1, 'rawAudio.wav')
            fanSpeed = pn.predict('trimedAudio.wav')
            
            fanSpeedNum = numberToInt(fanSpeed)
            print(fanSpeedNum)
            
            fullPhrase += fanSpeed 
            print(fullPhrase)

            """
            # Send string request to server
            values = {'word': fullPhrase}
            requests.post(                                            
                URL,
                headers=headers,
                json=values
            )
            # Send int request to server
            values = {'device': deviceNum, 'action': actionNum}
            requests.post(                                            
                URL,
                headers=headers,
                json=values
            )
            """

        
        else:
            # Get action to perform
            print("#################\nDo you want to turn the device on or off?\n#################")
            input("Press ENTER to record  your voice...")
            recordVoice(FORMAT, channels, sample_rate, True, True, chunk)
            trimAudio.trimAudio(1, 'rawAudio.wav')
            pa = Predict_Action()
            action = pa.predict('trimedAudio.wav')

            actionNum = actionToInt(action)
            print(actionNum)

            fullPhrase += action

            print(deviceNum, actionNum)
            print(fullPhrase)

            """
            # Send string request to server
            values = {'word': fullPhrase}
            requests.post(                                            
                URL,
                headers=headers,
                json=values
            )
            # Send int request to server
            values = {'device': deviceNum, 'action': actionNum}
            requests.post(                                            
                URL,
                headers=headers,
                json=values
            )
            """
        
        # Check if the user wants to continue with the process
        cntStr = input("Press Q to terminate the process, Press any key to continue interacting... PRESS ENTER after your input.\n")
        if cntStr == "Q" or cntStr == "q":
            isContinue = False
        else:
            continue

    print("PROCESS TERMINATED.")