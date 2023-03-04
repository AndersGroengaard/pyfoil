from bs4 import BeautifulSoup  
import re 

def create_airfoil_database(output_folder="./foil_lib/"):
    """
    ---------------------------------------------------------------------------
    |    Function for downlaoding all airfoil dat files from:                 |
    |    www.m-selig.ae.illinois.edu                                          |
    ---------------------------------------------------------------------------
    """
    
    try:
        import urllib.request as urllib2
    except ImportError:
        import urllib2
    
   
    path = "https://m-selig.ae.illinois.edu/ads/coord_seligFmt/"               # Base filepath for the UIUC airfoil website (used for accessing .dat files)
    
    # Open the webpage and create the soup
    html_page = urllib2.urlopen(path)                                          # Open the URL
    soup = BeautifulSoup(html_page, 'lxml')                                    # Create the soup
    dat_files = soup.find_all('a', attrs={'href': re.compile('\.dat', re.IGNORECASE)})
    n_files = len(dat_files) 
 
    i = 1                                                                      # Iteration counter
    links = []																   # Initialize list of links for appending
    
    for dat in dat_files:                                                      # Loop over all the  links on webpage ending on ".dat"
        links.append(dat.get('href'))							   		       # Append the link to the list 
        file_url = path + dat.get('href')
        foil_data_filename = dat.get('href').rsplit('/', 1)[-1]
        output_file_path = output_folder+foil_data_filename
        urllib2.urlretrieve(file_url, output_file_path) 
        print("Retrieving file number: "+str(i)+ " of "+str(n_files)+ " : "+foil_data_filename)
        i += 1
        
        
  
if __name__ == "__main__":
    create_airfoil_database()