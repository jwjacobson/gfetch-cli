# Privacy Policy for GFetch

*Last Updated: 2025-07-25*

## 1. Introduction

This Privacy Policy describes how GFetch ("we," "our," or "the Application") handles your information when you use our Gmail email download application. We are committed to protecting your privacy and ensuring transparency about our data practices.

## 2. Information We Access

### 2.1 Gmail Data
When you use GFetch, the Application accesses:
- Email messages (including headers, body, and metadata)
- Email attachments
- Email addresses (sender and recipient information)
- Email dates and subjects

### 2.2 Authentication Data
- Google OAuth 2.0 tokens (stored locally on your device)
- Your Google account email address (for authentication purposes)

## 3. How We Use Your Information

GFetch uses your Gmail data solely to:
- Authenticate your Google account
- Download emails you select
- Save emails and attachments to your local device
- Format and organize downloaded content

**We do NOT:**
- Store your data on external servers
- Share your data with third parties
- Use your data for advertising or marketing
- Analyze your email content for any purpose beyond downloading

## 4. Data Storage and Security

### 4.1 Local Storage Only
All data accessed by GFetch is stored exclusively on your local device in the following formats:
- Raw emails (.eml files)
- Cleaned emails (.txt files)
- Attachments (original formats)
- OAuth tokens (JSON format)

### 4.2 No Cloud Storage
GFetch does not transmit, upload, or store any of your data on cloud servers or external systems.

### 4.3 Security Measures
- OAuth tokens are stored in a separate file with restricted permissions
- The Application uses Google's secure OAuth 2.0 flow for authentication
- All data transmission occurs directly between your device and Google's servers using HTTPS

## 5. Data Retention

- **Downloaded emails**: Retained on your device until you manually delete them
- **OAuth tokens**: Retained until you revoke access or delete the token file
- **No server retention**: Since we don't use servers, we don't retain any of your data

## 6. Your Rights and Controls

You have complete control over your data:

### 6.1 Access Control
- You choose which email addresses to download emails from
- You can stop the download process at any time

### 6.2 Data Deletion
- Delete downloaded emails using the Application's delete function
- Remove OAuth tokens by deleting the token.json file
- Revoke access through your Google Account settings

### 6.3 Data Portability
- All downloaded emails are in standard formats (.eml, .txt)
- You can move, copy, or transfer files as needed

## 7. Google API Services Compliance

GFetch's use of Google API Services complies with the [Google API Services User Data Policy](https://developers.google.com/terms/api-services-user-data-policy), including the Limited Use requirements.

### 7.1 Limited Use Disclosure
GFetch's use and transfer of information received from Google APIs adheres to Google API Services User Data Policy, including the Limited Use requirements. We only use Gmail data to provide the email download functionality you've requested.

### 7.2 Scope of Access
GFetch only requests read-only access to Gmail (`https://www.googleapis.com/auth/gmail.readonly`) and cannot modify or delete your emails on Gmail servers.

## 8. Third-Party Services

GFetch uses:
- **Google Gmail API**: To access your email data (governed by Google's Privacy Policy)
- **Google OAuth 2.0**: For secure authentication

No other third-party services are used.

## 9. Children's Privacy

GFetch is not intended for use by children under 13 years of age. We do not knowingly collect information from children under 13.

## 10. Open Source Transparency

GFetch is open-source software. You can review our source code at:
https://github.com/jwjacobson/gfetch-cli

This transparency allows you to verify our privacy practices.

## 11. Changes to This Policy

We may update this Privacy Policy from time to time. Changes will be indicated by updating the "Last Updated" date. Continued use of the Application after changes constitutes acceptance of the updated policy.

## 12. Data Breach Notification

Since GFetch doesn't store your data on servers, the risk of a data breach is limited to your local device. However, if we become aware of any security vulnerability in the Application that could compromise your local data, we will:
- Post a notice on our GitHub repository
- Release a security update as soon as possible

## 13. International Data Transfers

GFetch does not transfer data internationally. Your data remains on your local device in your jurisdiction.

## 14. Contact Information

For questions about this Privacy Policy or our privacy practices, contact:

Jeff Jacobson  
Email: jeffjacobsonhimself@gmail.com  
GitHub: https://github.com/jwjacobson/gfetch-cli

## 15. Additional Rights

Depending on your location, you may have additional privacy rights under laws such as GDPR or CCPA. Since your data is stored locally and never transmitted to us, you maintain full control over exercising these rights.

## 16. Compliance Statement

This Privacy Policy is designed to comply with:
- Google API Services User Data Policy
- General Data Protection Regulation (GDPR)
- California Consumer Privacy Act (CCPA)
- Other applicable privacy laws and regulations