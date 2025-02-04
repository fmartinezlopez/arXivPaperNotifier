import os
import yaml
from arxiv import Client, Search, SortCriterion
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def load_config(config_path='config.yml'):
    """
    Load search parameters from YAML configuration file.
    
    :param config_path: Path to the YAML config file
    :return: Dictionary with configuration parameters
    """
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config['search']

def search_arxiv_papers(primary_keyword, optional_keywords, categories=None, days=7, n_buffer=100):
    """
    Search for arXiv papers published in the last N days.
    
    :param primary_keyword: Keyword that MUST be present
    :param optional_keywords: List of optional keywords
    :param categories: List of arXiv categories to filter (e.g., ['hep-ex', 'hep-ph'])
    :param days: Number of days to look back
    :return: List of matching papers
    """

    # Construct the default API client.
    client = Client()

    # Calculate the date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    # Construct the base query with the primary keyword
    base_query = f'ti:"{primary_keyword}" OR abs:"{primary_keyword}"'
    
    # Add optional keywords if provided
    if optional_keywords:
        optional_query = " OR ".join([
            f'ti:"{kw}" OR abs:"{kw}"' for kw in optional_keywords
        ])
        full_query = f'({base_query}) AND ({optional_query})'
    else:
        full_query = base_query

    # Add category filtering if specified
    if categories:
        category_query = " OR ".join([f'cat:{cat}' for cat in categories])
        full_query += f' AND ({category_query})'

    # Search for the N most recent articles matching the keyword(s)
    search = Search(
        query = full_query,
        max_results = n_buffer,
        sort_by = SortCriterion.SubmittedDate
    )

    # Filter papers published in the last N days
    matching_papers = []
    for result in client.results(search):
        if result.published.replace(tzinfo=None) >= start_date:
            matching_papers.append({
                'title': result.title,
                'summary': result.summary[:1000] + '...' if len(result.summary) > 1000 else result.summary,
                'link': result.entry_id,
                'authors': ', '.join(author.name for author in result.authors),
                'category': result.primary_category
            })

    return matching_papers

def send_email(sender_email, sender_password, recipient_email, papers):
    """
    Send an email with the list of matching papers.
    
    :param sender_email: Email address sending the notification
    :param sender_password: Email account password or app-specific password
    :param recipient_email: Email address receiving the notification
    :param papers: List of papers to include in the email
    """

    # Create message container
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = f"arXiv Paper Notification - {len(papers)} New Papers"
    
    # Construct email body
    body = "Recent arXiv Papers:\n\n"
    for paper in papers:
        body += f"Title: {paper['title']}\n"
        body += f"Authors: {paper['authors']}\n"
        body += f"Category: {paper['category']}\n"
        body += f"Abstract: {paper['summary']}\n"
        body += f"Link: {paper['link']}\n\n"
    
    # Attach body to email
    msg.attach(MIMEText(body, 'plain'))
    
    # Send email
    try:
        # Use your email provider's SMTP server (example for Gmail)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

def main():

    # Load configuration
    try:
        config = load_config()
    except Exception as e:
        print(f"Error loading configuration: {e}")
        return

    # Get email credentials from environment variables
    SENDER_EMAIL = os.environ.get('SENDER_EMAIL')
    SENDER_PASSWORD = os.environ.get('SENDER_PASSWORD')
    RECIPIENT_EMAIL = os.environ.get('RECIPIENT_EMAIL')

    if not all([SENDER_EMAIL, SENDER_PASSWORD, RECIPIENT_EMAIL]):
        print("Missing required email credentials in environment variables")
        return
    
    # Search for papers using configuration
    papers = search_arxiv_papers(
        primary_keyword=config['primary_keyword'],
        optional_keywords=config['optional_keywords'],
        categories=config['categories'],
        days=config['days_back']
    )
    
    # Send email if papers found
    if papers:
        send_email(SENDER_EMAIL, SENDER_PASSWORD, RECIPIENT_EMAIL, papers)
    else:
        print("No matching papers found.")

if __name__ == "__main__":
    main()