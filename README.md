# ml_streamlit_template

Example:
![How it works](<docs/Screenshot 2024-12-12 at 3.29.08 PM.png>)

The command to run directly on local machine is `streamlit run app.py --server.port=8501` or `streamlit run app.py`

Alternatively, you can use `docker compose build` and `docker compose up -d` for local deployment

Note that for hosting, it is likely that the server does not work under a proxy since I am using the STUN server. In that case, please customise it according to the docs based on streamlit_webRTC library.
