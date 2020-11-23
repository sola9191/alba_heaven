import os
import csv
import requests
from bs4 import BeautifulSoup

os.system("clear")
alba_url = "http://www.alba.co.kr"

request = requests.get(alba_url)
soup = BeautifulSoup(request.text, "html.parser")
super_brand = soup.find("div", {"id":"MainSuperBrand"})
brand_box = super_brand.find("ul", {"class":"goodsBox"})
brand_list = brand_box.find_all("li")


def get_url(brand_a):
  link_name = brand_a.find("a")["href"]
  file_name = brand_a.find_all("span")[1].text
  print(link_name)
  print(file_name)
  
  return file_name, link_name
 

def get_info(link_name):
   
    request = requests.get(link_name)
    soup = BeautifulSoup(request.text, "html.parser")
    
    rows = soup.find("div", {"id":"NormalInfo"}).find("tbody").find_all("tr", class_= {"divide", ""})
    job_info = []
    try:
      for row in rows:       
          location = row.find_all("td")[0].text     
          title = row.find_all("td")[1].find("span").text
          time = row.find_all("td")[2].text
          pay = row.find_all("td")[3].text
          date = row.find_all("td")[4].text
          job_info.append(
          {  "location":location,
              "title":title,
              "time":time,
              "pay":pay,
              "date":date
            }      
          )

    except IndexError:  
      job_info.append(row.find_all("td")[0].text)

    return job_info
    
      
    
     
def save_file(file_name, job_info):
  file = open(f"{file_name}.csv", mode="w")

  writer = csv.writer(file)
  writer.writerow(["place", "title", "time", "pay", "date"])
  for job in job_info:
    if(type(job) == str):
      writer.writerow(f"{job}")
    else:
      writer.writerow(list(job.values()))
  
  return   


def main():
  for brand_a in brand_list:
    url_info = get_url(brand_a)
    print(url_info)
    job_list = get_info(url_info[1])
    save_file(url_info[0], job_list)
    
main()




