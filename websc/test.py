from websc.websc import FlipkartScraper, AmazonScraper





print("Fetching Amazon Data...")
AmazonScraper("https://www.amazon.in/s?k=freez+uder+budejet&crid=1QA86ZWTF6E3Q&sprefix=freez+uder+budejet%2Caps%2C320&ref=nb_sb_noss")

print("\nFetching Flipkart Data...")
FlipkartScraper("https://www.flipkart.com/search?q=laptop+under+35000")
