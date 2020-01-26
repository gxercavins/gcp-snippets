# MP3 Audio Encoding

Example, using the Python Client library, to specify MP3 as the input audio format. Originally written as an answer to this [StackOverflow question](https://stackoverflow.com/a/59838848/6121516).

## Example

In order to select `RecognitionConfig.AudioEncoding.MP3`, we'll need to use the [`v1p1beta1`][1] version. We'll base our example in the quickstart code [here][2]. No changes are needed to the pip command (`pip install --upgrade google-cloud-speech`) but we need to import the right version (`speech_v1p1beta1`) in our Python code:

```python
# [START speech_transcribe_streaming]
def transcribe_streaming(stream_file):
    """Streams transcription of the given audio file."""
    import io
    from google.cloud import speech_v1p1beta1
    from google.cloud.speech_v1p1beta1 import enums
    from google.cloud.speech_v1p1beta1 import types
    client = speech_v1p1beta1.SpeechClient()
```

And now we can choose the MP3 encoding:

```python
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.MP3,
        sample_rate_hertz=16000,
        language_code='en-US')
    streaming_config = types.StreamingRecognitionConfig(config=config)
```

Full code in `mp3.py` file. Output for the included MP3 sample:

```bash
$ python mp3.py sample.mp3
Finished: True
Stability: 0.0
Confidence: 0.9875912666320801
Transcript: I'm sorry Dave I'm afraid I can't do that
```

Tested with `google-cloud-speech==1.3.1`.


  [1]: https://cloud.google.com/speech-to-text/docs/reference/rest/v1p1beta1/RecognitionConfig#audioencoding
  [2]: https://github.com/GoogleCloudPlatform/python-docs-samples/blob/ddb79a72126bf5f5773145c8ebb91cf01d71432c/speech/cloud-client/transcribe_streaming.py



## License

These examples are provided under the Apache License 2.0.

## Issues

Report any issue to the GitHub issue tracker.
