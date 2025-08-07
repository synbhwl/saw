## Welcome to SAW (stupid assignment writer)

SAW is a minimal FastAPI-based tool to generate assignments (mainly) or quick contents in markdown-style HTML writeups.

### How to Use

To use the app, just open the URL in your browser and add query parameters directly in the address bar:
```
https://my-domain.com/make?topic=Your+Topic+Here&words=500&tone=academic
```

### Parameters:
- topic (required): The subject or title you want content about.
- words (optional): Approximate word count. Default is 500.
- tone (optional): Writing tone. Default is natural academic.

**Example:**
```
https://my-domain.com/make?topic=Photosynthesis&words=300&tone=conversational
```

You will receive a clean HTML page with markdown-style content based on your input.

### Source Code

GitHub Repository: [https://github.com/synbhwl/saw](https://github.com/synbhwl/saw)
