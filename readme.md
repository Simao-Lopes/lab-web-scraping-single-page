![logo](https://raw.githubusercontent.com/Simao-Lopes/lab-web-scraping-single-page/master/Logo/Gnoosic.PNG)

# Your best song suggesting tool

## Usage  
   
The main component is the file 05 - User Randomizer. Just run the script type a song that you like and a nice song will be sugested, either from our top hits list or from our curated list.  
A spotify direct link will be provided.

## Developer instructions

#### Files included
   
- 01 - Web scraper. This script scraps the web for the best top100 playlists and saves them into a dataset for further usage in the main script.
- 02 - Spotify. Gets a massive list of songs from spotify, if you want to add some new playlists just run the script inserting a line in the end of the 5th cell following this structure.
'''
playlist_df.loc[len(playlist_df.index)] = ['Your playlist Name', 'playlist URI']
'''
- 03 - Clustering. This script clusters our big database previously built in the 02 script using KNN cluster model with 8 nodes. Be aware that you must pickle both the new clustering model and the transformer to be used in the main script. Warning: executing this takes really long, use only if the main dataset is changed or has to be recalculated.
- 04 - Get Hot songs URI on spotify. This script gets all the uri for our top100 dataset, and appends a nex column before saving it to a csv file so that in the main script we can sugest a link. 
- 05 - User randomizer. The main script, execute and enjoy.
- **app.py.** Using a Streamlit instance you can run this script and run the project as a web based app. Run first a terminal with the code
''' 
streamlit run app.py 
'''

##### Folders

- Data. Stores all the csv's used on the project. 
- Logo. Folder for the logo of our app.
- Model_data. Stores the models and transformers needed, please don't remove.

## Used techologies

- Spotify API
- Python
- Streamlit

## License

This is an educational project, all materials can be used freelly.
