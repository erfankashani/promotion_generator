import os
from dotenv import load_dotenv
from openai import OpenAI
import json
import re
from helper.utils import Website, generate_html_page


def validate_open_ai_api_key(api_key:str):
    if not api_key:
        raise ValueError("No API key was found; please set an OPENAI_API_KEY environment variable")
    elif not api_key.startswith("sk-proj"):
        raise ValueError("An API key was found, but it doesn't start sk-proj-; please check you're using the right key")
    elif api_key.strip() != api_key:
        raise ValueError("An API key was found, but it looks like it might have space or tab characters at the start or end - please remove them")
    else:
        print("API key looks good")


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
validate_open_ai_api_key(api_key)

MODEL = 'gpt-4o-mini'
openai = OpenAI()


class Crawler:
    def __init__(self, url):
        self.url = url
        self.system_prompt = self.get_system_prompt()


    def get_system_prompt(self) -> str:
        system_prompt = "you are provided with a list of links found on a webpage. \
        you are able to decide which of the links would be most relevent to include in a promotion brochure about the company, \
        such as links to an about, or a company page, or Careers/Jobs pages. \n"
        system_prompt += "you should respond in JSON as in this example:"
        system_prompt += """
        {
            "links": [
                {"type": "about", "url": "https://www.example.com/about"},
                {"type": "careers", "url": "https://www.example.com/careers"}
            ]
        }
        """
        return system_prompt


    def get_links_user_prompt(self, website: Website) -> str:
        user_prompt = f"Here is the list of links on the website {website.url} - "
        user_prompt += "please decide which of these links are relevant web links for a brochure about the company, respond with the full http URL in JSON format."
        user_prompt += "Links (some might be relative links): \n"
        user_prompt += "\n".join(website.links)
        return user_prompt


    def messages_for_links(self, website: Website) -> list:
        return [
            {
                "role": "system",
                "content": self.system_prompt
            },
            {
                "role": "user",
                "content": self.get_links_user_prompt(website)
            }
        ]


    def get_links(self):
        website = Website(self.url)
        response = openai.chat.completions.create(
            model=MODEL,
            messages=self.messages_for_links(website),
            response_format={"type": "json_object"}
        )
        result = response.choices[0].message.content
        return json.loads(result)


    # make the promotion brochure
    def crawl_website(self):
        result = "Landing page:\n"
        result += Website(self.url).get_contents()
        links = self.get_links()
        print("Found links:", links)
        for link in links["links"]:
            result += f"\n\n{link['type']}\n"
            result += Website(link["url"]).get_contents()
        return result


def get_promotion_system_prompt(promotion_reason: str) -> str:
    return f"""
            You are a marketing specialist that analyzes the contents of several relevant pages from a company website
            system_prompt = f"You are a marketing specialist that analyzes the contents of several relevant pages from a company website
            and creates an effective promotion brochure depengin on the company's product or service type for prospective customers, investors and recruits. Respond in markdown.
            The promotion occasion is: {promotion_reason}. Include details about the company culture, customers and promotion reason if you have the information.
            """


def get_promotion_user_prompt(company_name: str, url: str, promotion_reason: str) -> str:
    website_info = Crawler(url)
    user_prompt = f"You are looking at a company called: {company_name}\n"
    user_prompt += f"Here are the contents of its landing page and other relevant pages; use this information to build a short promotion deal for {promotion_reason} in markdown.\n"
    user_prompt += website_info.crawl_website()
    user_prompt = user_prompt[:20_000] # Truncate if more than 20,000 characters
    return user_prompt


def create_promotion_text(company_name:str, url:str, promotion_reason:str) -> str:
    response = openai.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": get_promotion_system_prompt(promotion_reason = promotion_reason)},
            {"role": "user", "content": get_promotion_user_prompt(company_name = company_name, url = url, promotion_reason = promotion_reason)}
          ],
    )
    return response.choices[0].message.content


def create_img_prompt(promotion_text:str, promotion_reason:str) -> str:
    img_user_prompt = f"the following is the promotion deal text for a business related to {promotion_reason} - "
    img_user_prompt += "please write a one liner prompt that generates an apealing image for the promotion deal based on deal content and promotion reason:"
    img_user_prompt += promotion_text
    print(img_user_prompt)
    
    response = openai.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "you are a graphic designer tasked with write a one liner prompt that best suits the advertisement text. Avoid using text in the photo."},
            {"role": "user", "content": img_user_prompt}
          ],
    )
    return response.choices[0].message.content


def create_promotion_img(img_prompt: str):
    response = openai.images.generate(
        model="dall-e-3",
        prompt=img_prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    return response.data[0].url


def execute(company_name: str, url:str, promotion_reason:str):
    promotion_text = create_promotion_text(company_name=company_name, url=url, promotion_reason=promotion_reason)
    print(promotion_text)

    img_prompt = create_img_prompt(promotion_text=promotion_text, promotion_reason=promotion_reason)
    print(img_prompt)

    img_url = create_promotion_img(img_prompt=img_prompt)
    print(img_url)

    final_markdown = f"![new img]({img_url})"
    final_markdown += f"\n{promotion_text}"

    generate_html_page(markdown_str=final_markdown, file_name="promotion.html")


if __name__ == "__main__":
    # company_name = "Apple"
    # url = "https://apple.com"
    # promotion_reason = "Black Friday"

    # ask user for the company url
    company_name = input("Please enter the name of the company you'd like to analyze:")
    url = input("Please enter your desired company URL to analyze:")
    promotion_reason = input("Please enter the occation for the promotion you'd like to create (ex. Black Friday):")
    execute(company_name=company_name, url=url, promotion_reason=promotion_reason)

