from bs4 import BeautifulSoup
import requests
import markdown

class Website:
    """
    A utility class to represent a Website that we have scraped
    """

    def __init__(self, url):
        self.url = url
        response = requests.get(url)
        self.body = response.content
        soup = self.get_soup(body=self.body)
        self.title = soup.title.string if soup.title else "No title found"
        self.text = soup.body.get_text(strip=True) if soup.body else ""
        self.links = self.get_links(soup=soup)


    def get_soup(self, body , page_type: str = 'html.parser') -> BeautifulSoup:
        soup = BeautifulSoup(body, page_type)
        if soup.body:
            for irrelevant in soup.body(["script", "style", "img", "input"]):
                irrelevant.decompose()
        return soup


    def get_links(self, soup: BeautifulSoup) -> list:
        return [link.get('href') for link in soup.find_all('a')]


    def get_contents(self) -> str:
        return f"Webpage Title:\n{self.title}\nWebpage Contents:\n{self.text}\n\n"


def generate_html_page(markdown_str: str, file_name: str) -> None:
    """
        Generate an HTML page from a markdown string
    """
    html = markdown.markdown(markdown_str)
    try:
        with open(file_name, 'w') as file:
            file.write(html)
        print(f"HTML page generated successfully in the path: {file_name}")
    except Exception as e:
        print(f"Error writing to file: {e}")