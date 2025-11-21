
import os
import json
import webbrowser
from datetime import datetime
from openai import OpenAI
import markdown

# ==========================================
# CONFIGURATION
# ==========================================
# Retrieve API key from environment variable for security
API_KEY = os.environ.get("PERPLEXITY_API_KEY")

# Model selection: 'sonar-pro' is best for complex research and reasoning.
# Use 'sonar' for faster, cheaper results.
MODEL_NAME = "sonar-pro"

def get_deals(query, budget, personality):
    """
    Connects to Perplexity API to find real-time deals.
    """
    if not API_KEY:
        return "Error: Perplexity API Key not found. Please set the PERPLEXITY_API_KEY environment variable."

    client = OpenAI(api_key=API_KEY, base_url="https://api.perplexity.ai")

    print(f"\n🔎 Sniper is scanning the web for: {query}...")
    print(f"💰 Max Budget: BDT{budget}")
    print(f"🧠 Personality Profile: {personality}")
    print("Please wait, this may take 10-20 seconds (I'm reading live news)...")

    # We ask for JSON format to make parsing easier, but Perplexity is chatty,
    # so we'll ask for a specific Markdown structure that we can easily convert to HTML.
    system_prompt = (
        "You are an expert deal hunter and shopping assistant. "
        "Your goal is to find CURRENTLY ACTIVE sales and deals. "
        "Do not list items at full price unless they are exceptionally good value. "
        "You must verify that the deals are recent (from the last 7 days). "
        "Format your response as a list of items. For each item, provide: "
        "1. Product Name "
        "2. Original Price vs Sale Price "
        "3. A one-sentence reason why this fits the user's personality "
        "4. A direct URL citation."
    )

    user_prompt = (
        f"Find me 5 amazing gift ideas for someone who is into: {personality}. "
        f"They are looking for: {query}. "
        f"My hard limit budget is BDT {budget}. "
        "Focus on items that are currently on sale or have a price drop. "
        "Provide the output in this specific format for each item:\n\n"
        "## [Product Name]\n"
        "**Price:** [Sale Price] (Was [Original Price])\n"
        "**Why:** [Reason]\n"
        "**Link:** [URL]\n\n"
    )

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def generate_html_report(content, query):
    """
    Creates a beautiful, simple HTML file with the results and returns the HTML content.
    """
    # Simple parsing to make links clickable if they aren't already
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Deal Sniper Report: {query}</title>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, \"Segoe UI\", Roboto, Helvetica, Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 40px; background: #f4f4f9; }}
            .container {{ background: white; padding: 40px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }}
            h1 {{ color: #2d3748; border-bottom: 2px solid #e2e8f0; padding-bottom: 20px; }}
            .timestamp {{ color: #718096; font-size: 0.9em; margin-bottom: 30px; display: block; }}
            .deal-content {{ line-height: 1.6; color: #4a5568; }}
            h2 {{ color: #2b6cb0; margin-top: 30px; }}
            strong {{ color: #2d3748; }}
            a {{ color: #3182ce; text-decoration: none; font-weight: bold; }}
            a:hover {{ text-decoration: underline; }}
            .footer {{ margin-top: 40px; font-size: 0.8em; color: #a0aec0; text-align: center; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎯 Deal Sniper Report: {query}</h1>
            <span class="timestamp">Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</span>
            <div class="deal-content">
                {content.replace('\n', '<br>')}
            </div>
            <div class="footer">
                Powered by Perplexity Sonar Pro
            </div>
        </div>
    </body>
    </html>
    """

    # Use markdown library if available, otherwise simple replacement
    try:
        html_body = markdown.markdown(content)
        # Inject the body into our template
        final_html = html_content.replace(f"{content.replace(chr(10), '<br>')}", html_body)
    except ImportError:
        # Fallback if markdown lib not installed
        final_html = html_content
    
    # Removed file writing and browser opening functionality for Flask integration
    return final_html
