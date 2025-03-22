# TeeCustomizer Ordering Assistant

This project implements a chatbot interface for an agent that guides users through a customized t-shirt ordering process.


## Project Structure

### Directories Overview

- **`chatbot`**  
  Contains code related to the assistant logic.

- **`chromadb`**  
  A vector database with FAQ documents.

- **`data`**  
  Contains raw and processed FAQ and customization info data.

- **`logs`**  
  Contains logged support system messages.

- **`notebooks`**  
  Contains notebooks for particular tasks (e.g., updating the FAQ file, etc.).

## Using Docker
If you want to build the image with Docker, you should change the paths in the config.py file to:
```
CHROMADB_PATH = r"/app/chromadb"
LOGSDIR_PATH = r"/app/logs"
```

## Setup Instructions (Windows)

Have been tested against Python 3.11.

1. **Edit the .env file, enter your OpeanAI API key**

```OPENAI_API_KEY=SOME_VALUE```

2. **Create a Virtual Environment**

Terminal:

```py -m venv .venv```

3. **Activate the Virtual Environment**

Terminal:

```.venv\Scripts\activate```

4. **Install Dependencies**

Ensure that you have a requirements.txt file in the project root, then run:

```pip install -r requirements.txt```

5. **Run the Application**

Start the application by executing:

```chainlit run app.py```

