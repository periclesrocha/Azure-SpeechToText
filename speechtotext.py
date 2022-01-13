# conda create --name AzureSpeechToText python=3.8
# C:\Users\procha\Anaconda3\envs\AzureSpeechToText\Scripts\pip.exe install azure-cognitiveservices-speech
import azure.cognitiveservices.speech as speechsdk
import os
import sys
import time

# Replace with your own subscription key and service region (e.g., "westus").
speech_key, service_region = '<key>', '<region>'

def runSpeechToText(inputFile, outputFile):
    audioFile = inputFile

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    audio_config = speechsdk.audio.AudioConfig(filename=audioFile)
    # Change the 'language' parameter to your desired language 
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, language="en-US", audio_config=audio_config)

    done = False

    def stop_cb(evt):
        """callback that signals to stop continuous recognition upon receiving an event `evt`"""
        print('CLOSING on {}'.format(evt))
        nonlocal done
        done = True

    # Writes the recognized text into a text file with the same name as the audio file name
    def write_ln(text, outFile):
        with open(outFile, "a+") as file:
            file.seek(0, os.SEEK_END)
            file.write(text)
            file.write('\n')

    # Connect callbacks to the events fired by the speech recognizer    
    # Print the recognized text... 
    speech_recognizer.recognized.connect(lambda evt: print('{}'.format(evt.result.text)))
    # ... and also write it to the output file.
    speech_recognizer.recognized.connect(lambda evt: write_ln(evt.result.text,outputFile))
    speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))
    # stop continuous recognition on either session stopped or canceled events
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    # Start continuous speech recognition
    speech_recognizer.start_continuous_recognition()
    while not done:
        time.sleep(.5)

    speech_recognizer.stop_continuous_recognition()
    # </SpeechContinuousRecognitionWithFile>

if (len(sys.argv)) > 2: # If parameters passed, see if it is accepted
    print(len(sys.argv))
    inputFile = sys.argv[1].lower()
    outputFile = sys.argv[2].lower()
    runSpeechToText(inputFile, outputFile)
else:
    print('Please provide an audio file to convert and the name of the desired transcription file. Usage: speechtotext.py inputaudiofilename outputtextfilename')