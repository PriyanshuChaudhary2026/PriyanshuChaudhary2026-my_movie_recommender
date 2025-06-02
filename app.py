from flask import Flask, request, render_template
import pickle

app = Flask(__name__)

# ------------------ Load Pickle ------------------
with open('movie_recommender.pkl', 'rb') as f:
    df, cv, similarity = pickle.load(f)

# ------------------ Recommendation Logic ------------------
def recommend(movie):
    movie = movie.lower()
    results = {'found': False, 'input_movie': '', 'recommendations': []}

    if movie not in df['Movie Name_lower'].values:
        return results

    movie_index = df[df['Movie Name_lower'] == movie].index[0]
    results['input_movie'] = df.loc[movie_index, 'Movie Name']
    results['found'] = True

    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])
    movies_list = [i for i in movies_list if i[0] != movie_index][:5]

    for i in movies_list:
        recommended_movie = df.iloc[i[0]]['Movie Name']
        recommended_tags = df.iloc[i[0]]['formatted_tags']
        similarity_score = i[1]

        results['recommendations'].append({
            'movie': recommended_movie,
            'tags': recommended_tags,
            'score': f"{similarity_score:.4f}"
        })

    return results

# ------------------ Routes ------------------
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        movie_name = request.form['movie_name'].strip()
        results = recommend(movie_name)
        return render_template('index.html', results=results, search_query=movie_name)
    return render_template('index.html', results=None, search_query=None)

# ------------------ App Start ------------------
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
