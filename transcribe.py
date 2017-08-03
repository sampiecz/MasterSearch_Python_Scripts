def transcribe_gcs(gcs_uri):
    """Asynchronously transcribes the audio file specified by the gcs_uri."""
    import time
    from google.cloud import speech
    speech_client = speech.Client()

    audio_sample = speech_client.sample(
        content=None,
        source_uri=gcs_uri,
        encoding='AMR',
        sample_rate_hertz=8000)

    operation = audio_sample.long_running_recognize('en-US')

    retry_count = 100
    while retry_count > 0 and not operation.complete:
        retry_count -= 1
        time.sleep(2)
        operation.poll()

    if not operation.complete:
        print('Operation not complete and retry limit reached.')
        return
    file_name = conversation_partner + ".txt"
    output_file = open(file_name, 'w')
    alternatives = operation.results
    for alternative in alternatives:
        print('Transcript: {}'.format(alternative.transcript))
        print('Confidence: {}'.format(alternative.confidence))
        output_file.write(alternative.transcript)
        output_file.write(str(alternative.confidence))

    output_file.close()
    # [END send_request_gcs]
conversation_partner = input("Who were you talking to? : ")
path = input("What is the url of the audio file you would like transcribed? : ")
transcribe_gcs(gcs_uri=path)
