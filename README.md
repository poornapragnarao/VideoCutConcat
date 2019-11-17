# Video cut and concatenate
Simple video clip concatenation. Open a video, select start and end points and process. Concatenates all the start-end pair clips and creates a new video.

# Requirements

This requires opencv(and dependencies like ffmpeg) and python to be installed in the system.

# Usage

1. Run the script ```python viditcv.py```
2. Keys - 
   ```i``` to save current frame.

   ```spacebar``` to pause.

   ```,``` for previous frame.
   
   ```.``` for next frame.
   
   ```m``` to go back 5 frames.
   
   ```/``` to go forward 5 frames.
   
3. Hit ```'s'``` on the frame from where you want to clip the video.

4. Hit ```'e'``` on the frame where you want the clip to end.

5. Repeat as necessary.

6. Hit ```'q'``` or ```'p'``` to concatenate and save the video in the same path as chosen video file.



