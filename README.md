# nasa-ex
retrieve list of  larger than 1000kb files by query of "Ilan Ramon" from NASA library

This script queries NASA'a Image and Video library with a hard coded query string : "Ilan Ramon"
it then get's a collection of asset objects. each of those has a collection link that holds a metadata link as well.

by querying those metalinks for every asset object the script looks for assets that has size greater than 1000kb.
After finding all relevant asets it then writes the results to a /csv file: "ilan_ramon.csv" 

This script uses Python3 with various libs - this repo also contains a virtual python env - so no need to download Python3 or install any libraries for it.

# Future Enhancements would be:
1. Make query as an argument instead of hard coded.
2. Make API key read from a remote file or other remote asset.
3. The script takes about 7 minutes to run - find a way to shorten calls to API/Library.
