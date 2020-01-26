# Progress Percent

Example, using the Python Client library, to track progress status for a long-running operation. Originally written as an answer to this [StackOverflow question](https://stackoverflow.com/a/57560663/6121516).

## Example

We'll base our code on a callback-approach, such as the one in [here](https://googleapis.dev/python/speech/latest/gapic/v1/api.html), to access `Operation.metadata.progress_percent` while waiting for the operation to complete. As an example here we check the progress every 5s:

```python
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
```

Output example (note that in this case I used a public audio file which is short and it goes from 0 to 100% straight away):

```python
Progress: 0%
...
Progress: 0%
results {
  alternatives {
    transcript: "it\'s okay so what am I doing here why am I here at GDC talking about VR video it\'s because I believe my favorite games I love games I believe in games my favorite games are the ones that are all about the stories I love narrative game design I love narrative-based games and I think that when it comes to telling stories in VR bring together capturing the world with narrative based games and narrative based game design is going to unlock some of the killer apps and killer stories of the medium"
    confidence: 0.959626555443
  }
}
results {
  alternatives {
    transcript: "so I\'m really here looking for people who are interested in telling us or two stories that are planning projects around telling those types of stories and I would love to talk to you so if this sounds like your project if you\'re looking at blending VR video and interactivity to tell a story I want to talk to you I want to help you so if this sounds like you please get in touch please come find me I\'ll be here all week I have pink hair I work for Google and I would love to talk with you further about VR video interactivity and storytelling"
    confidence: 0.954977035522
  }
}

Progress: 100%
```

All code in `progress.py` file.

## License

These examples are provided under the Apache License 2.0.

## Issues

Report any issue to the GitHub issue tracker.
