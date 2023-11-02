import gzip
import json
import tempfile

import requests


# Obtain the JSON data
def main():
    found_cves = []
    for year in range(2002, 2024):

        url = f"https://nvd.nist.gov/feeds/json/cve/1.1/nvdcve-1.1-{year}.json.gz"  # https://nvd.nist.gov/feeds/json/cve/1.1/nvdcve-1.1-recent.json.gz"
        response = requests.get(url)
        # Save the JSON feed in a temporary file
        with tempfile.TemporaryFile() as temp:
            temp.write(response.content)  # save gzip contents to file
            temp.seek(0)  # reset the file handler to the beginning of file
            with gzip.open(temp, 'rb') as f:
                file_content = f.read()
                data = json.loads(file_content)

                # Extract the relevant information
                for entry in data['CVE_Items']:
                    cve_id = entry['cve']['CVE_data_meta']['ID']
                    cve_description = entry['cve']['description']['description_data'][0]['value']
                    cve_description = " ".join(cve_description.lower().replace(",", " ").split(" "))
                    references = entry['cve']['references']
                    if "regular expression denial of service" in cve_description.lower() or "redos" in cve_description.lower():
                        for reference in references['reference_data']:
                            if "https://github.com" in reference['url']:
                                found_cves.append(entry)
                                break

    with(open("redos_cves_with_github.json", "w")) as f:
        json.dump(found_cves, f, indent=4)


if __name__ == '__main__':
    main()
