from flask import Flask, render_template, request, redirect,session,flash,url_for
from collections import defaultdict
app =Flask(__name__)

app.config.from_pyfile('config.py')

votes= defaultdict(int)
voters= set()
candidates= ["John Doe", "Jane Smith", "Harry George", "Alice Mark"]

@app.route('/')
def index():
    return render_template('index.html', candidates=candidates, votes=votes)

@app.route('/vote', methods=['POST'])
def vote():
    name= request.form['name']
    candidate= request.form['candidate']
    if name in voters:
        flash('You have already voted')
        return render_template('index.html', candidates=candidates, votes=votes)

        
    if candidate in candidates:
        votes[candidate] += 1
        session['voted']= True
        voters.add(name)
        flash('Thank you for voting!')
        return render_template('index.html', candidates=candidates, votes=votes)

        
    else:
        flash('Invalid candidate.')
        return render_template('index.html', candidates=candidates, votes=votes)

        
@app.route('/results')
def results():
    return render_template('results.html', candidates=candidates, votes=votes)
if __name__ =="__main__":
    app.run(host='0.0.0.0', port =5000, debug=True)