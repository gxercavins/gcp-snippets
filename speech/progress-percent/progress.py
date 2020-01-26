import time

from google.cloud import speech_v1
from google.cloud.speech_v1 import enums


client = speech_v1.SpeechClient()

encoding = enums.RecognitionConfig.AudioEncoding.FLAC
sample_rate_hertz = 16000
language_code = 'en-US'
config = {'encoding': encoding, 'sample_rate_hertz': sample_rate_hertz, 'language_code': language_code}
uri = 'gs://gcs-test-data/vr.flac'
audio = {'uri': uri}

response = client.long_running_recognize(config, audio)

def callback(operation_future):
    result = operation_future.result()
    progress = response.metadata.progress_percent
    print(result)

response.add_done_callback(callback)

progress = 0

while progress < 100:
	try:
		progress = response.metadata.progress_percent
		print('Progress: {}%'.format(progress))
	except:
		pass
	finally:
		time.sleep(5)
