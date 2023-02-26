from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
browser = webdriver.Chrome(service=Service(    ChromeDriverManager().install()), options=chrome_options)

# options = Options()
# options.add_argument("--no-sandbox")
# options.add_argument("--disbale-dev-shm-usage")

# browser = webdriver.Chrome(options=options)

def get_page_counts(term):
  url = f"https://ca.indeed.com/jobs?q={term}"
  browser.get(url)
  if browser.page_source:
    soup = BeautifulSoup(browser.page_source, "html.parser")
    pagination = soup.find("nav", class_="css-jbuxu0 ecydgvn0")
    pages = pagination.find_all('div')
    count = len(pages)
    if count == 0:
      return 1
    elif count >=5:
      return 5
    else:
      return count-1

def extract_indeed_jobs(term):
  pages = get_page_counts(term)
  print("Found", pages, "pages")
  results = []
  for page in range(pages):
    final_url = f"https://ca.indeed.com/jobs?q={term}&start={page*10}"
    print("Requesting...", final_url)
    browser.get(final_url)
    if browser.page_source:
      soup = BeautifulSoup(browser.page_source, "html.parser")
      job_list = soup.find('ul', class_="jobsearch-ResultsList")
      jobs = job_list.find_all('li', recursive=False)
      for job in jobs:
        zone = job.find('div', class_="mosaic-zone")
        if zone == None:
          anchor = job.select_one('h2 a')
          title = anchor.find('span')
          link = anchor['href']
          company = job.find('span', class_="companyName")
          region = job.find('div', class_="companyLocation")
          if region.string == None:
            location = "More than one location"
          else:
            location = region.string
          tags = job.find('div', class_="attribute_snippet")
          if tags == None:
            salary = "TBD"
          else:
            if '$' in tags.text:
              salary = tags.text
            else:
              salary = "TBD"
          # print(salary)
          # print('/////\n/////')
          job_data = {
            'position': title.string.replace(",", " "),
            'company': company.string.replace(",", " "),
            'salary': salary.replace(",", " "),
            'location': location.replace(",", " "),
            'link': f"https://ca.indeed.com{link}",
          }
          results.append(job_data)
    else:
      print("Can't get jobs.")
  return results