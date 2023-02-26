from bs4 import BeautifulSoup
import requests

def extract_rmok_jobs(term):
  url = f"https://remoteok.com/remote-{term}-jobs"
  request = requests.get(url, headers={"User-Agent": "Kimchi"})
  if request.status_code == 200:
    results = []
    soup = BeautifulSoup(request.text, "html.parser")
    jobs = soup.find_all("tr", class_="job")
    # print(len(jobs))
    for job_section in jobs:
      job_posts = job_section.find_all('td', class_="company")
      # print(job_posts)
      for post in job_posts:
        anchor = post.find('a')
        link = anchor['href']
        title = post.find('h2', itemprop="title")
        company = post.find('h3', itemprop="name")
        # print(company.string)
        tags = post.find_all('div', class_="location")
        region = tags[0]
        for i, tag in enumerate(tags):
          # print("i", i)
          # print("tag", tag)
          if "$" in tag.string:
            salary = tags[i]
        job_data = {
          'position': title.string.strip().replace(",", " "),
          'company': company.string.strip().replace(",", " "),
          'salary': salary.string.replace(",", " "),
          'location': region.string.replace(",", " "),
          'link': f"https://remoteok.com/{link}",
        }
        results.append(job_data)
    return results
  else:
    print("Can't get jobs.")