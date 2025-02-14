# TeeCustomizer Ordering Assistant

This project implements a chatbot interface for an agent that guides users through a customized t-shirt ordering process.

Demo can be temporarily accessible from here:
http://16.16.173.120:8000/

## Setup Instructions (Windows)

1. **Create .env file and enter your OpeanAI API key into it**

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

```chainlit run main.py```

## Next Steps to Implement

### 1. Other Architecture for Improved Reliability
- Transitioning to a more reliable architecture could enhance overall performance and stability.
- Reducing the architecture to a simple router with modifications may improve robustness.

### 2. User Query Decomposition
- For more robust user request handling, decompose user queries into sub-queries.
- Each sub-query will be handled separately to improve error handling and scalability.

### 3. Store Vector Database on the Cloud
- Currently, the vector database (VDB) is hosted in the same container as the application.
- Hosting the VDB on a separate server would provide better control over database updates and scaling.

### 4. Overall Implementation Improvements
- Some application elements are tightly coupled, making the system harder to maintain.
- Refactoring the code is necessary to improve modularity and maintainability.

### 5. Overall Logging Improvements
- Error logging needs enhancements for better debugging and issue tracking.
- Implement logging of `user_id` for the `support_logging` tool by extracting it from the graph state.

### 6. Ordering Tool
- Create a db with user orders.
- Add tool to place the order into database of purchases.

### 7. Improve Prompts
- Currently prompts are suboptimal, due to the lack of testing.
- Prompts should be optimized.

### 8. Add LangSmith support for tracking

### 9. Create a CI/CD pipeline.
