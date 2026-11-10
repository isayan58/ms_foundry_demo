"""
For more samples please visit https://github.com/Azure-Samples/cognitive-services-speech-sdk
"""

import azure.cognitiveservices.speech as speechsdk

endpoint_url = "https://ws-ms-foundry.cognitiveservices.azure.com/"

from urllib.parse import urlparse
from dotenv import load_dotenv
import os

load_dotenv()

parsed = urlparse(endpoint_url)
base_endpoint = f"{parsed.scheme}://{parsed.netloc}"

speech_key = os.getenv("API_KEY")
speech_config = speechsdk.SpeechConfig(subscription=speech_key, endpoint=base_endpoint)
speech_config.speech_synthesis_voice_name = "en-US-EmmaMultilingualNeural"
# Receive uncompressed audio so the SDK doesn't need to start a local decoder
# (avoids "Codec decoding is not started within 2s").
speech_config.set_property(
    speechsdk.PropertyId.SpeechServiceConnection_SynthEnableCompressedAudioTransmission, "false"
)

# use the default speaker as audio output.
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

text = "Hello, welcome to Azure AI Foundry! I'm Emma, How can I help you today?"

result = speech_synthesizer.speak_text_async(text).get()

# Check result
if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
    print("Speech synthesized for text [{}]".format(text))
elif result.reason == speechsdk.ResultReason.Canceled:
    cancellation_details = result.cancellation_details
    print("Speech synthesis canceled: {}".format(cancellation_details.reason))
    if cancellation_details.reason == speechsdk.CancellationReason.Error:
        print("Error details: {}".format(cancellation_details.error_details))
