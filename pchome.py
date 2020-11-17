import requests
import argparse
import json
import time

baseurl = "https://24h.pchome.com.tw"


def getMAC(productID,cookie):
    headers = {}
    headers['Cookie'] = cookie
    r = requests.get(baseurl+
                     "/prod/cart/v1/prod/"+
                     productID+
                     "-000/snapup",
                     headers=headers)
    res = json.loads(r.text)
    return res['MAC'], res['MACExpire'], res['Status']

def addCart(productID, mac, expire, cookie):
    headers = {
            "Referer": "https://24h.pchome.com.tw/prod/",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/86.0.4240.193 Safari/537.36"
    }
    headers['Cookie'] = cookie
    # TI 000 as no choose, 001 as first choose, 002 as second...
    data_tmp = {
        "G":[],
        "A":[],
        "B":[],
        "TB":"24H",
        "TP":2,
        "T":"ADD",
        "TI":productID+"-000",
        "RS":productID.split("-")[0],
        "YTQ":1,
        "CAX":mac,
        "CAXE":expire
    }
    data = {'data':json.dumps(data_tmp)}
    r = requests.post(baseurl+"/fscart/index.php/prod/modify",
                      headers=headers, 
                      data=data)
    print(r.text)
    response = json.loads(r.text)
    if response["PRODADD"]=='1':
        print("product added")
        print("price total: " + str(response["PRODTOTAL"]))
        r = 1
    else:
        print("add failed")
        r = 0
    return r

def main():
    while(1):
        parser = argparse.ArgumentParser()
        parser.add_argument("productID", help="enter the productID found from the end of the PCHOME url")
        parser.add_argument("-c", "--cookie",  help="enter cookie with name of ECC and ECWEBSESS")
        args = parser.parse_args()

        if args.cookie:
            cookie = args.cookie
        else:
            cookie = ""
        productID = args.productID
        mac, expire, status = getMAC(productID, cookie)
        if status == 'OK':
            print("adding to cart...")
            r = addCart(productID, mac, expire, cookie)
            if r: break
        else:
            print("not available yet")
        time.sleep(0.5)

if __name__ == '__main__':
    main()
