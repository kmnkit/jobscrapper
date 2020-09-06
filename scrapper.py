import requests
from bs4 import BeautifulSoup


def get_soup(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    return soup


def get_last_page(url):
    soup = get_soup(url)
    pages = soup.find("div", {"class": "s-pagination"}).find_all("a")
    last_page = pages[-2].find("span").get_text(strip=True)
    return int(last_page)


def get_so_jobs(job_name):
    so_jobs = []
    url = f"https://stackoverflow.com/jobs?r=true&q={job_name}"
    so_last_page = get_last_page(url)
    for page in range(so_last_page):
        soup = get_soup(f"{url}&pg={page+1}")
        results = soup.find_all("div", {"class": "-job"})
        for r in results:
            title = r.find("h2").find("a")["title"]
            company = (
                r.find("h3").find_all("span", recursive=False)[0].get_text(strip=True)
            )
            job_id = r["data-jobid"]
            so_jobs.append(
                {
                    "title": title,
                    "company": company,
                    "link": f"https://stackoverflow.com/jobs?id={job_id}",
                }
            )
        print(f"StackOverflow {page+1}페이지째 스크랩완료...")
    return so_jobs


def get_wework_jobs(job_name):
    ww_jobs = []
    url = f"https://weworkremotely.com/remote-jobs/search?term={job_name}"
    soup = get_soup(url)
    features = (
        soup.find("section", {"class": "jobs"})
        .find("ul")
        .find_all("li", {"class": "feature"})
    )
    for feature in features:
        feature_detail = feature.find("a", recursive=False)

        title = feature_detail.find("span", {"class": "title"}).text
        company = feature_detail.find("span", {"class": "company"}).text
        link = f'https://weworkremotely.com{feature_detail["href"]}'

        ww_jobs.append(
            {
                "title": title,
                "company": company,
                "link": link,
            }
        )
    print("Wework Job 스크랩 완료")
    return ww_jobs


def get_ro_jobs(job_name):
    ro_jobs = []
    base_url = "https://remoteok.io"
    url = f"https://remoteok.io/remote-dev+{job_name}-jobs"
    soup = get_soup(url)
    trs = soup.find_all("tr", {"class": "job"})
    for tr in trs:
        try:
            td = tr.find_all("td", {"class": "company"})[0]
            title = td.find("h3").text
            company = td.find("h2").text
            link = td.find("a", {"class": "preventLink"})["href"]
            ro_jobs.append(
                {
                    "title": title,
                    "company": company,
                    "link": base_url + link,
                }
            )
        except:
            print(title)
            print("태그를 찾지 못하여 다음으로 넘어갑니다.")
            continue
    print("Remote Only 스크랩 완료")
    return ro_jobs


def get_all_jobs(job_name):
    so_jobs = get_so_jobs(job_name)
    ww_jobs = get_wework_jobs(job_name)
    ro_jobs = get_ro_jobs(job_name)
    return so_jobs, ww_jobs, ro_jobs
