## Stupid Assignment writer

A very fast assignment/content writer with built in prompts. Can be used directly through the browser URL bar. Uses Groq API ('llama-3.1-8b-instant' and 'llama-3.3-70b-versatile'), takes user inputs through query parameters and returns clean HTML in md format. Built with FastAPI.

### How to Use

To use the app, open the URL in your browser and add query parameters directly in the address bar:

*https://saw-production.up.railway.app/make?topic=Your+Topic+Here&words=500&tone=academic*


Here:

- topic=You+topic+here is a **mendatory** parameter. Replace the example with your own topic.
- words=500 is an **optional** parameter. You can choose not to write this and stick with the default 500 words.
- tone=academic is also an **optional** parameter. You can stick with the default 'natural academic'

(saparate each word of your topic/tone by a '+' symbol. Eg: Indus Valley Civilization becomes Indus+Valley+Civilization and separate each parameter with a '&' symbol. Eg: words=500&tone=academic)

### More about parameters:
- topic (required): The subject or title you want content about. Must be less than 1000 characters. Clear and specific topic is recommended.
- words (optional): Approximate word count. Default is 500. Must be less than 3000.
- tone (optional): Writing tone. Default is natural academic. Must be less than 100 characters. Avoid long tone names.

Since words and tone are optional, you can write a simple request as:


*https://saw-production.up.railway.app/make?topic=Photosynthesis*


You will receive a clean HTML page with markdown-style content based on your input.

### Source Code

GitHub Repository for more info: [https://github.com/synbhwl/saw](https://github.com/synbhwl/saw)
