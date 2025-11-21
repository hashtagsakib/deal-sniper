from flask import Flask, render_template, request, render_template_string
import deal_hunter
import os

app = Flask(__name__)

# The API key should be set as an environment variable on the hosting platform,
# NOT hardcoded here, especially not when pushing to a public Git repository.
# The line that assigned the API key has been removed.

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    item = request.form['item']
    budget = request.form['budget']
    personality = request.form['personality']

    # Call the get_deals function
    raw_deals_content = deal_hunter.get_deals(item, budget, personality)

    # Generate the full HTML report using the modified function
    final_html_report = deal_hunter.generate_html_report(raw_deals_content, item)

    # Render the HTML report directly
    return render_template_string(final_html_report)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
