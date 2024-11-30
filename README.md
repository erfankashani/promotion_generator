# Promotion Generator

This project uses Frontier omnichannel LLMs to crawl a given website, understand the business area, customers, team business type. The program then generates a creative promotional text based on the event the user specifies, uses the promotion to generate prompt for an image generation model, and finally builds an image for the promotional brochure which then is turned into a webpage for viewing. 

# sample Execution of the script
```bash
- Please enter the name of the company you like to analyze:apple
- Please enter your desired company URL to analyze:https://www.apple.com/
- Please enter the occation for the promotion you like to create (ex. Black Friday):black friday

#Internal Notes
Found links: {'links': [{'type': 'about', 'url': 'https://www.apple.com/contact/'}, {'type': 'careers', 'url': 'https://www.apple.com/careers/us/'}, {'type': 'investor', 'url': 'https://investor.apple.com/'}, {'type': 'newsroom', 'url': 'https://www.apple.com/newsroom/'}, {'type': 'leadership', 'url': 'https://www.apple.com/leadership/'}, {'type': 'diversity', 'url': 'https://www.apple.com/diversity/'}, {'type': 'environment', 'url': 'https://www.apple.com/environment/'}, {'type': 'privacy', 'url': 'https://www.apple.com/legal/privacy/'}]}

```
# Resulting Promotion


![](images/sample_3.png)

# 🎉 Apple Black Friday Promotion 🎉

## Experience the Magic of Apple this Black Friday! 

At **Apple**, we are excited to bring exclusive offers to our customers this Black Friday! Join us in celebrating the season of giving and innovation.

### 🍏 Special Offers 
- **Get an Apple Gift Card up to $200!**  
  With every eligible purchase, enjoy a gift card on us! This offer is valid from **November 29 to December 2**, 2024. **Limited availability!**  

- **Up to $1000 in Credit on New iPhones!**  
  Take advantage of our incredible trade-in deals when you purchase the latest **iPhone 16 Pro** or **iPhone 16** series. Perfect for upgrading your tech!

- **Support a Great Cause!**  
  Apple is committed to making a difference! For every purchase made with **Apple Pay**, we’ll donate $5 to the **Global Fund** to fight AIDS from now through **December 8, 2024**. 

### 🕒 Hurry, While Supplies Last!
These promotions won’t last forever. Visit your nearest **Apple Store** or shop online to secure your gift of technology and help us make an impact in the lives of others.

### 🌟 A Culture of Innovation and Sustainability
At Apple, we believe in creating products that improve lives while caring for our planet. Our culture is built around inclusion, sustainability, and continuous innovation. When you choose Apple, you are part of a community that embraces creativity and responsibility.

### 💬 Join Us!
Make this Black Friday special by choosing **Apple**. Browse our full range of products, from the latest iPhones to the innovative Apple Watch and MacBook. Experience the seamless integration of technology designed for your lifestyle!

**Don’t miss out on this opportunity!** Act fast and seize these deals!

---

### For Help or More Information
Visit our **Support** page or contact your nearest Apple Store for assistance.


# Install
```bash
conda env create -f environment.yml
conda activate llms
python promotion_generator.py
# after the scrip is done you can look at the results in promotion.html