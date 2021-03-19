# audacity-selection-cutter

Audicity selection cutter. 

For all audicity projects in current directory cuts audio files by audacity selection.   
Audio file must be in the same directory with filename as in project. Requires extension as its not saved anywhere.   
"But why do I even need it???" - you say.   
Well Im glad you asked.     
The thing is I want to cut those files without recoding them (and possibly lose quality) with nice GUI. And it was simpler to write stupid script than look for proper program online so...

Also this way tags are also copied :)   
Basically runs: 
```
ffmpeg -ss SELECTIONS_START -t SELECTION_DURATION -i FILENAME.EXTENSION -acodec copy FILENAME-cut.EXTENSION
```

So... you need ffmpeg...
