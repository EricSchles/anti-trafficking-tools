# Overall architecture

The architecture of this project will be broken out into three pieces.  The first is going to be the web scrapers which exist in AWS Lambda containers that spin up as needed.  The second piece will be a persistent application with modeling code and bitcoin analysis.  


## The Web scrapers

The webscrapers will be spun up as needed within cron jobs and run on an adhoc basis.  They scrape backpage and potentially other sources.

## The modeling code and bitcoin analysis

The modeling code looks at understanding writing styles of different users and compares them to do link analysis.  The bitcoin analysis does link analysis along a different avenue to see if various wallets are related to specific posts on backpage.

