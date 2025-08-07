## Welcome to SAW (stupid assignment writer)

SAW (stupid assignment writer) is just a simple FastAPI-based tool to generate assignments (mainly) or quick contents in markdown-style HTML writeups.

### How to Use

To use the app, just open the URL in your browser and add query parameters directly in the address bar:
```
https://saw-production.up.railway.app/make?topic=Your+Topic+Here&words=500&tone=academic
```

(saparate each word of your topic/tone by a + symbol. Eg: Indus Valley Civilization becomes Indus+Valley+Civilization)

### Parameters:
- topic (required): The subject or title you want content about.
- words (optional): Approximate word count. Default is 500.
- tone (optional): Writing tone. Default is natural academic.

**Example:**
```
https://saw-production.up.railway.app/make?topic=Photosynthesis&words=300&tone=conversational
```

> *Do remember that the words and tone parameters are optional*

So a simple request can be 
```
https://saw-production.up.railway.app/make?topic=Photosynthesis
```

You will receive a clean HTML page with markdown-style content based on your input.