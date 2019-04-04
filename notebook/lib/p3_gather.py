# import urllib.request as req
#import certifi
#from urllib.request import urlopen
import requests
import os
from pathlib import Path



def download_data(reference_dict, overwrite=False):
    '''
        download a copy of a web page to local file storage
        ref: https://docs.python.org/3/library/urllib.request.html#module-urllib.request
        url is internet address of data
        out_filename is name of local file containing data
        overwrite forces the data file to be overwritten or left alone
        
    '''
    
    for r in reference_dict:
        ref = reference_dict[r]

        if ref['type'] == 'data':
            out_filename = ref['local']

            if overwrite :
                os.remove(out_filename)

            url = ref['url']

            # download from internet if file doesn't already exist on drive
            # or overwrite if flag set to True
            the_file = Path(out_filename)

            if not the_file.is_file():
                r = requests.get(url, stream=True)
                the_file.is_file()
                with open(out_filename, 'wb') as fd:
                    for chunk in r.iter_content(chunk_size=128):
                        fd.write(chunk)


def main():
    print('###############################')
    reference_dict= {
            "type": "data",
            "title": "",
            "provider": "plotly",
            "period": "",
            "website": "https://plot.ly/python/sankey-diagram/",
            "url": "https://raw.githubusercontent.com/plotly/plotly.js/master/test/image/mocks/sankey_energy.json",
            "local": "sankey_energy.json",
            "exports": {
                "condensed": "<csv_output_filename>",
                "fields": [
                    {"field_in": "<col-name>", "field_out": "<col-name>", "function": ""}
                ]
            },
            "transforms": {

            }
        }
    
    download_data(const['references'])

if __name__ == "__main__":
    # execute only if run as a script
    main()