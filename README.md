# diaporama_maker  
Allows you to make diaporama from your videos (Works better using Linux) 
## Setup  
You will have to install all dependencies using requirements.txt and to use python 3.9   
``pip install -r requirements.txt``

Your repository of video have to look as :  
|  
->Anime_name  
|  
----->S[number]    
|  
--------->ep[number].mp4  
|  
->Other_anime_name  
....  
  
## Launch script  
This script is customisable using commandline arguments :  
### Linux
```shell  
python ./extract.py --it 20 --pathIn "../../Videos/" --pathOut "./output/" --startTimeParam 0 20 10 --timeBetweenFramesParam 2 10 60 --exept "TEST" "Repo_test" "Bug"    
```  
### Windows  
```shell 
python C:\Users\oreil\Desktop\diaporama_maker\extract.py --it 2 --pathIn "Z:\Anim" --pathOut "C:\\Users\\oreil\\Desktop\\diaporama_maker\\output\\" --startTimeParam 0 20 10 --timeBetweenFramesParam 2 10 60 --exept "Boruto"
```
This command make 20 times frames extraction using specified paths, specified times (start and delay between 2 frames) and skip some other bad animes
