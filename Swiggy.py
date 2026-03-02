import json
from datetime import datetime
from Swiggy_database import send_to_db
from pprint import pprint

products=[]
basepath="https://instamart-media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,h_600/"

def input_file(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
        # pprint(data)
        return data

def parser(d):
    for i in d["data"]["cards"]:
        for j in i["card"]["card"]["gridElements"]["infoWithStyle"]["items"]:
            for k in j["variations"]:
                product={}
                product["name"]=k.get("displayName")
                product["Prod_id"]=k.get("skuId")
                product["Prod_price"]=float(k.get("price").get("offerPrice").get("units"))
                product["Prod_quantity"]=k.get("quantityDescription")
                product["Image_URL"]=k.get("imageIds")
                product["Image_URL"]=[basepath+image for image in product["Image_URL"]]
                product["Discount_per"]=int(k.get("price").get("offerApplied").get("listingDescription").split("%")[0])
                product["mrp"]=float(k.get("price").get("mrp").get("units"))
                product["In_stock"]=k.get("inventory").get("inStock")

                products.append(product)
    return products


file=input("enter file name: ")
d=input_file(file)
extracted=parser(d)
send_to_db(extracted)