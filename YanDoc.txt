Check version:
	cmd: py || python
	install: py -m pip install pinecone-client
	môi trường ảo env: pip install pinecone-client

Tạo môi trường ảo: 
	python -m venv myenv || py -m venv venv
Kích hoạt môi trường ảo:
	myenv\Scripts\activate
Cài đạt Kaggle:
	pip install Kaggle
Thoát môi trường ảo: 
	deactivate
Sử dụng lệnh Kaggle:
	kaggle datasets download ryanrudes/yttts-speech
	Nó sẻ down về file zip

pip install pinecone-client
pip install sentence-transformers (chuyển đổi ngôn ngữ)
pip install flask(framework)
pip install flask-cors
pip install datasets
pip install tqdm

pip install streamlit(giao diện)
demo: streamlit run app.py

=> (*) : khi cài 1 số thư viện thì khi dùng python của soft store ko chạy được, ví dụ như (sentence-transformers) -> vào manage app .... -> tắt hết python app (có lẽ được cài ở soft store) trong này, tắt luôn cả  App installer-> mục đích là để bản python được cài trực tiếp trên máy có thể hoạt động.





















