# ArXiv Paper Notifier

Automatically receive email notifications about new arXiv papers matching your keywords and categories. This script runs weekly using GitHub Actions and sends you a digest of relevant papers.

## Features

- 🔍 Search for papers by keywords
- 📋 Filter by arXiv categories (e.g., hep-ex, hep-ph)
- 📧 Receive weekly email digests
- 🔐 Secure credential handling
- ⚡ Powered by GitHub Actions
- 💰 Completely free to use

## Setup Instructions

### 1. Fork this Repository
Click the "Fork" button at the top right of this repository to create your own copy.

### 2. Set Up Gmail
You'll need a Gmail account with an App Password:

1. Enable 2-Step Verification on your Google Account:
   - Go to your [Google Account Security Settings](https://myaccount.google.com/security)
   - Find "2-Step Verification" and follow the setup process

2. Create an App Password:
   - Go back to Security Settings
   - Scroll to "App passwords" (appears only after enabling 2-Step Verification)
   - Select "Mail" for app and "Other" for device
   - Give it a name (e.g., "ArXiv Notifier")
   - Copy the generated 16-character password

### 3. Configure GitHub Secrets
Add your email credentials as secrets in your forked repository:

1. Go to your forked repository's Settings
2. Click "Secrets and variables" → "Actions"
3. Add the following secrets by clicking "New repository secret":
   - Name: `SENDER_EMAIL`
     Value: Your Gmail address
   - Name: `SENDER_PASSWORD`
     Value: Your 16-character Gmail App Password
   - Name: `RECIPIENT_EMAIL`
     Value: Email address where you want to receive notifications

### 4. Customize Your Search
Edit `arxiv_paper_notifier.py` to modify your search preferences:

```python
# Configuration section in main()
PRIMARY_KEYWORD = 'neutrino'  # Change this to your main keyword
OPTIONAL_KEYWORDS = ['oscillation', 'interaction']  # Add related keywords
CATEGORIES = ['hep-ex', 'hep-ph']  # Change to your preferred categories
DAYS_BACK = 7  # Adjust the number of days to look back
```

Common arXiv categories:

   - hep-ex: High Energy Physics - Experiment
   - hep-ph: High Energy Physics - Phenomenology
   - hep-th: High Energy Physics - Theory
   - nucl-ex: Nuclear Experiment
   - nucl-th: Nuclear Theory
   - astro-ph: Astrophysics

### 5. Enable GitHub Actions

1. Go to the "Actions" tab in your forked repository
2. Click the green button to enable workflows
3. The script will now run automatically every Monday at 8:00 AM UTC

## Testing Your Setup

1. Go to the "Actions" tab
2. Select "ArXiv Paper Notifier" workflow
3. Click "Run workflow"
4. Check your email for results

## Troubleshooting

- No emails received?

    - Verify your Gmail App Password is correct
    - Check GitHub Actions logs for errors
    - Make sure the secrets are properly set
    - Check your spam folder

- Wrong papers?

    - Adjust your keywords and categories
    - Modify the search criteria in the script

## Support

- For issues with the script: Open an issue in this repository
- For Gmail issues: Check Google Account Help
- For GitHub Actions issues: Check GitHub Actions Documentation

## Contributing
Contributions are welcome! Feel free to:

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License
This project is licensed under the MIT License - feel free to use it for any purpose.