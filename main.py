
from fastapi import FastAPI, HTTPException, status, Request
from fastapi.responses import HTMLResponse
from typing import Optional
from jinja2 import Template
import os
from dotenv import load_dotenv
from groq import Groq
import json
import markdown
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

load_dotenv()
api_key = os.getenv('GROQ_API_KEY').strip() # adding the strip() after the server stopped working
# just because i had a tailing newline after the key
debug = os.getenv('DEBUG') == "true"
model = ('llama-3.1-8b-instant' if debug else 'llama-3.3-70b-versatile')
# current even in production i am keeping the model as 'instant' simply because
# it works well and has a better request limit

app = FastAPI()

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

client = Groq(api_key=api_key)

# this is the home route and it's basically a readme typa thing
# i am using jinja2 to fill the placeholders
@app.get('/')
async def show_home():
    try:
        with open('docs/home.md', 'r') as f:
            content_raw = f.read()
        content_formatted = markdown.markdown(content_raw)
        with open('docs/template.html', 'r') as ft:
            html_template = Template(ft.read())
        full_html = html_template.render(content=content_formatted)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="you did nothing wrong, my app just can't read some files"
        )
    return HTMLResponse(content=full_html)

# this is a monolith route, i know
# but there aren't many repeated logic for much generalization
# the ones that are, i kept them for explicitness, it's a very small app afterall
@app.get("/make")
@limiter.limit("2/minute")
async def make_assignment(
    request: Request,
    topic: Optional[str] = None,
    words: Optional[int] = 500,
    tone: Optional[str] = "netural academic"
):
    if not topic:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Oops! you forgot to add the topic. eg: my_url/make?topic=something"
        )

    if len(topic) > 1000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="My God, that's a long ass topic. Please tone it down"
        )

    if words and words > 3000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="My God, word limit too high. Please keep it less tan 3000"
        )

    if tone and len(tone) > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="My God, never seen such a lengthy tone. Please tone it down to less than 100 characters"
        )

    if words:
        try:
            if words < 1500:
                with open('docs/def_prompt.txt', 'r') as f:
                    template = Template(f.read())
            if words >= 1500 and words <= 3000:
                with open('docs/ab1500.txt', 'r') as f:
                    template = Template(f.read())
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="you did nothing wrong, my app just can't read some files"
            )

    prompt = template.render(
        topic=topic,
        words=words,
        tone=tone
    )

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{'role': 'user', 'content': prompt}]
        )
        content_raw = response.choices[0].message.content.strip()
        content_unformatted = content_raw.encode(
            'utf8').decode('unicode_escape')
        content_final = markdown.markdown(content_unformatted)

        with open('docs/template.html', 'r') as ft:
            html_template = Template(ft.read())
        full_html = html_template.render(content=content_final)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'something went wrong :( -> {str(e)}'
        )

    return HTMLResponse(content=full_html)
