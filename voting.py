from flask import Flask, render_template, request, flash, session
import csv
from collections import defaultdict

app = Flask(__name__)

# Secret key for session management
app.secret_key = 'your_secret_key'

# CSV file to store votes
CSV_FILE = 'votes.csv'

# Initialize candidates
candidates = ["John Doe", "Jane Smith", "Harry George", "Alice Mark"]

# Initialize voters set
voters = set()

# Load votes from CSV
def load_votes():
    votes = defaultdict(int)
    try:
        with open(CSV_FILE, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 2:  # Ensure the row has exactly 2 elements
                    candidate, count = row
                    votes[candidate] = int(count)
    except FileNotFoundError:
        # If the file does not exist, initialize it
        with open(CSV_FILE, mode='w') as file:
            writer = csv.writer(file)
            for candidate in candidates:
                writer.writerow([candidate, 0])
    return votes


# Save votes to CSV
def save_votes(votes):
    with open(CSV_FILE, mode='w') as file:
        writer = csv.writer(file)
        for candidate, count in votes.items():
            writer.writerow([candidate, count])

# Initialize votes
votes = load_votes()

@app.route('/')
def index():
    return render_template('index.html', candidates=candidates, votes=votes)

@app.route('/vote', methods=['POST'])
def vote():
    name = request.form['name']
    candidate = request.form['candidate']

    # Check if the user has already voted
    if name in voters:
        flash('You have already voted')
        return render_template('index.html', candidates=candidates, votes=votes)

    # Check if the candidate is valid
    if candidate in candidates:
        votes[candidate] += 1
        save_votes(votes)  # Save updated votes to CSV
        voters.add(name)
        flash('Thank you for voting!')
        return render_template('index.html', candidates=candidates, votes=votes)
    else:
        flash('Invalid candidate.')
        return render_template('index.html', candidates=candidates, votes=votes)

@app.route('/results')
def results():
    return render_template('results.html', candidates=candidates, votes=votes)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
