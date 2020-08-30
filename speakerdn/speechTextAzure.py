# import azure.cognitiveservices.speech as speechsdk
# def speech_text(audio_filename):
#     speech_key, service_region = "54fe015847d94db9a85672137c590286", "eastasia"
#     speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
#     audio_input = speechsdk.audio.AudioConfig(filename=audio_filename)

#     speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)

#     result = speech_recognizer.recognize_once()
#     if result.reason == speechsdk.ResultReason.RecognizedSpeech:
#         return result.text
#     elif result.reason == speechsdk.ResultReason.NoMatch:
#         return ""
#     elif result.reason == speechsdk.ResultReason.Canceled:
#         cancellation_details = result.cancellation_details
#         return ""

import speech_recognition as sr
def speech_text(audio_filename):
    try:
        import azure.cognitiveservices.speech as speechsdk
        speech_key, service_region = "54fe015847d94db9a85672137c590286", "eastasia"
        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
        audio_input = speechsdk.audio.AudioConfig(filename=audio_filename)

        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)

        result = speech_recognizer.recognize_once()
        print("azure")
        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            return result.text
        elif result.reason == speechsdk.ResultReason.NoMatch:
            return ""
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            return ""
    # In case if azure service not works 
    except:
        r = sr.Recognizer()
        with sr.AudioFile(audio_filename) as source:
            audio_listened = r.record(source)
            print("sr")
            # try converting it to text
            try:
                text = r.recognize_google(audio_listened)
                return text
            except sr.UnknownValueError as e:
                return ""