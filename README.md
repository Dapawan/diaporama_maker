# diaporama_maker  
Allows you to make diaporama from your videos (Linux system only) 
## Setup  
You will have to install all dependencies using requirements.txt    
``pip install -r requirements.txt``

Your repository of video have to look as :  
|  
->Anime_name  
|  
----->Anime_seasons    
|  
--------->Anime_episodes  
|  
->Other_anime_name  
....  
  
## Launch script  
This script is customisable using commandline arguments :
```shell  
python ./extract.py --it 20 --pathIn "../../Videos/" --pathOut "./output/" --startTimeParam 0 20 10 --timeBetweenFramesParam 2 10 60 --exept "TEST" "Repo_test" "Bug"    
```
This command make 20 times frames extraction using specified paths, specified times (start and delay between 2 frames) and skip some other bad animes
