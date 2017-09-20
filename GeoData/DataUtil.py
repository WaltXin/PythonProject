from urllib import request

def download_data(url):
    response = request.urlopen(url)
    csv = response.read()
    csv_str = str(csv)
    lines = csv_str.split("\\n")
    dest_url = r'data.csv'
    fx = open(dest_url, 'w')
    for line in lines:
        fx.write(line+'\n')
    fx.close()


def readFile(fileName):
    fr = open(fileName, 'r')
    text = fr.read()
    print(text)
    fr.close()