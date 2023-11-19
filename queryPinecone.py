from flask import Flask, jsonify, request
from flask_cors import CORS
import pinecone
from sentence_transformers import SentenceTransformer

app = Flask(__name__)
CORS(app)

def init_pinecone():
    pinecone.init(api_key="2b71f377-895a-4720-ad18-1fac4024c5ec", environment="gcp-starter")
    return pinecone.Index('youtube-search')

def init_retriever():
    return SentenceTransformer('flax-sentence-embeddings/all_datasets_v3_mpnet-base')

index = init_pinecone()
retriever = init_retriever()

@app.route("/api/home", methods=["GET"])
def home():
    query = request.args.get('query', default='', type=str)

    if query != "":
        xq = retriever.encode([query]).tolist()
        xc = index.query(xq, top_k=5, include_metadata=True)

        formatted_response = []
        for match in xc.matches:
            result = {
                'id': match.id,
                'title': match.metadata['title'],
                'url': match.metadata['url'],
                'thumbnail': match.metadata['thumbnail'],
                'score': match.score,
            }
            formatted_response.append(result)

        return jsonify({"results": formatted_response})
    else:
        
        return jsonify({"error": "No query provided"})

if __name__ == "__main__":
    app.run(debug=True, port=8080)
