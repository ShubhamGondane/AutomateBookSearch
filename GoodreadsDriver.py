import goodreads_api_client as gr
import config as config


client = gr.Client(developer_key=config.goodreads_access["key"], 
	developer_secret=config.goodreads_access["secret"],
	base_url="https://www.goodreads.com")
# client.authorize()
def getToRead():
	shelves = client.Shelf.list("94530768-shubham-gondane")
	to_read_dict = client.Review.list("94530768", "to-read", 50)
	books_list = []
	for book in to_read_dict["reviews"]["review"]:
		title = book["book"]["title"]
		authors_data = book["book"]["authors"]
		author = authors_data["author"]["name"]
		books_list.append([str(title), str(author)])
	return books_list
		
