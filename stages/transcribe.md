# Transcription — recording → text

A shared block for the stages Context and Voice. Read it when the stage has a recording but no text.

1. If there is a transcription skill (for example, `whisper`), call it with `Skill`.
   If the skill only describes the commands, run them yourself by the rules below.
2. If there is no skill, but there is `whisper-cli` and a model file (`ggml-*.bin`; check `$WHISPER_MODEL`,
   `~/.whisper/models`, `~/.cache/whisper`, `~/models`), transcribe it yourself, with timecodes (`-osrt`):
   the time per slide is calculated from them. Put temporary files into the scratchpad. If you do
   not find a model, do not download it silently: ask.
3. If there is neither, ask the person to paste the text of the transcript. Suggest tools:
   Handy, OpenSuperWhisper (local, model `large-v3`) or the built-in macOS dictation.
Save the transcript next to the recording (`<recording name>.md`). Do not edit the raw transcript — edit `slides.md`.
