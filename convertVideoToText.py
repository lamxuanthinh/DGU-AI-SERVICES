import os
import subprocess
import whisper

def convertVideoToAudio(input_file, output_file):
    ffmpeg_cmd = [
        "ffmpeg",
        "-i", input_file,
        "-vn",
        "-acodec", "libmp3lame",
        "-ab", "192k",
        "-ar", "44100",
        "-y",
        output_file
    ]

    try:
        subprocess.run(ffmpeg_cmd, check = True)
        print("Success")
    except subprocess.CalledProcessError as e:
        print("Conversion Failed")

def convertAudioToText(pathAudio):
    model = whisper.load_model("base")
    resultModel = model.transcribe(pathAudio, fp16=False)
    segments = resultModel.get('segments', [])
    main_folder = os.path.splitext(os.path.basename(pathAudio))[0]

    for segment in segments:
        start_time = segment.get('start', 0)
        end_time = segment.get('end', 0)
        
        formatted_start_time = "{:02d}.{:02d}.{:02d},{:03d}".format(
            int(start_time // 3600),
            int((start_time % 3600) // 60),
            int(start_time % 60),
            int((start_time - int(start_time)) * 1000)
        )

        formatted_end_time = "{:02d}.{:02d}.{:02d},{:03d}".format(
            int(end_time // 3600),
            int((end_time % 3600) // 60),
            int(end_time % 60),
            int((end_time - int(end_time)) * 1000)
        )


        folder_name = f"{formatted_start_time}-{formatted_end_time}"
        folder_path = os.path.join(main_folder, folder_name)
        os.makedirs(folder_path, exist_ok=True)

        formatted_start_time = formatted_start_time.replace(".", ":")
        formatted_end_time = formatted_end_time.replace(".", ":")
        formatted_start_time = formatted_start_time.replace(",", ".")
        formatted_end_time = formatted_end_time.replace(",", ".")

        # Cut audio based on start and end times
        output_audio_path = os.path.join(folder_path, f"audio.mp3")
        ffmpeg_cmd = [
            "ffmpeg",
            "-i", pathAudio,
            "-ss", formatted_start_time,
            "-to", formatted_end_time,
            "-c:a", "libmp3lame",  
            "-q:a", "2",          
            "-y",
            output_audio_path
        ]

        try:
            subprocess.run(ffmpeg_cmd, check=True)
            # print(f"Audio segment {formatted_start_time} to {formatted_end_time} saved successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to save audio segment {formatted_start_time} to {formatted_end_time}. Error: {e}")

        formatted_start_time = formatted_start_time.replace(".", ",")
        formatted_end_time = formatted_end_time.replace(".", ",")
        formatted_start_time = formatted_start_time.replace(":", ".")
        formatted_end_time = formatted_end_time.replace(":", ".")

        audio_path = os.path.join(main_folder, f"{formatted_start_time}-{formatted_end_time}", "audio.mp3")
        audio = whisper.load_audio(audio_path)
        audio = whisper.pad_or_trim(audio)

        mel = whisper.log_mel_spectrogram(audio).to(model.device)

        _, probs = model.detect_language(mel)
        print(f"Detected language: {max(probs, key=probs.get)}")

        options = whisper.DecodingOptions(fp16=False)
        resultWhisper = whisper.decode(model, mel, options)
        print(resultWhisper.text)

        file_path = os.path.join(folder_path, "subtitles.txt")
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(resultWhisper.text)


# Test
convertAudioToText("public/test/audio/paragraphVNTest.wav")
# convertAudioToText("public/test/audio/oneLineENAudioTest.mp3")
# convertAudioToText("public/test/audio/oneLineVNAudioTest.wav")
# convertAudioToText("public/test/audio/audio.mp3")
# convertVideoToAudio("public/test/video/paragraphTest.mp4", "audio.mp3")








