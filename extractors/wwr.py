from bs4 import BeautifulSoup
import requests


def extract_wwr_jobs(term):
  url = f"https://weworkremotely.com/remote-jobs/search?term={term}"
  request = requests.get(url, headers={"User-Agent": "Kimchi"})
  if request.status_code == 200:
    results = []
    soup = BeautifulSoup(request.text, "html.parser")
    jobs = soup.find_all("section", class_="jobs")
    for job_section in jobs:
      job_posts = job_section.find_all('li')
      job_posts.pop(-1)
      for post in job_posts:
        anchors = post.find_all('a')
        anchor = anchors[1]
        link = anchor['href']
        company, kind, region = anchor.find_all('span', class_="company")
        title = anchor.find('span', class_="title")
        job_data = {
          'position': title.string.strip().replace(",", " "),
          'company': company.string.strip().replace(",", " "),
          'salary': "TBD",
          'location': region.string.replace(",", " "),
          'link': f"https://weworkremotely.com{link}",
        }
        results.append(job_data)
    return results
  else:
    print("Can't get jobs.")