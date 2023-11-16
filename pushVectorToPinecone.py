import pinecone
from sentence_transformers import SentenceTransformer
from datasets import load_dataset
from tqdm.auto import tqdm

# set up pinecone. api_key and environment is created in pincone
pinecone.init(api_key="2b71f377-895a-4720-ad18-1fac4024c5ec", environment="gcp-starter")

# pinecone.create_index(
# 	'youtube-search',
#   	dimension=768, metric='cosine'
# )

# key "youtube-search is created in pinecone. Now will use"
index = pinecone.Index('youtube-search')

#pre-existing retriever model
#use MPNet
retriever = SentenceTransformer('flax-sentence-embeddings/all_datasets_v3_mpnet-base')
print(retriever)
#indexing
ytt = load_dataset(
    "pinecone/yt-transcriptions",
    split="train",
    revision="926a45"
)

batch_size = 64

for i in tqdm(range(0, len(ytt), batch_size)):
    i_end = min(i+batch_size, len(ytt))
    batch = ytt[i:i_end]
    embeds = retriever.encode(batch['text']).tolist()
    ids = [f"{x[0]}-{x[1]}" for x in zip(batch['video_id'], batch['start_second'])]
    meta = [{
        'video_id': x[0],
        'title': x[1],
        'text': x[2],
        'start_second': x[3],
        'end_second': x[4],
        'url': x[5],
        'thumbnail': x[6]
    } for x in zip(
        batch['video_id'],
        batch['title'],
        batch['text'],
        batch['start_second'],
        batch['end_second'],
        batch['url'],
        batch['thumbnail']
    )]
    to_upsert = list(zip(ids, embeds, meta))
    index.upsert(vectors=to_upsert)

