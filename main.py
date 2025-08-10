
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
# because i had a tailing newline after the key
debug = os.getenv('DEBUG') == "true"
model = ('llama-3.1-8b-instant' if debug else 'llama-3.3-70b-versatile')
# current even in production i am keeping the model as 'instant' because
# it works well and has a better request limit

app = FastAPI()

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

client = Groq(api_key=api_key)


@app.get('/')
async def show_home():
    try:
        with open('docs/home.md', 'r') as f:
            content_raw = f.read()
        content_formatted = markdown.markdown(content_raw)
        with open('docs/template.html', 'r') as ft:
            html_template = Template(ft.read())
        full_html = html_template.render(content=content_formatted)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"error: file read error: {str(e)}"
        )
    return HTMLResponse(content=full_html)

# may refactor the monolithic route into different functions
# keeping it currently because they are mostly non repetitive and only one main route exists 
@app.get("/make")
@limiter.limit("5/minute")
async def make_assignment(
    request: Request,
    topic: Optional[str] = None,
    words: Optional[int] = 500,
    tone: Optional[str] = "netural academic"
):
    if not topic:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="error: topic missing in query params. eg: https://saw-production.up.railway.app/make?topic=something"
        )

    if len(topic) > 1000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="error: topic too long, keep it under 100 characters."
        )

    if words and words > 3000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="error: word count too high, keep it under 3000 words."
        )

    if tone and len(tone) > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="error: tone too long, keep it under 100 characters"
        )

    if words:
        try:
            if words < 1500:
                with open('docs/def_prompt.txt', 'r') as f:
                    template = Template(f.read())
            if words >= 1500 and words <= 3000:
                with open('docs/ab1500.txt', 'r') as f:
                    template = Template(f.read())
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"error: file read error: {str(e)}"
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
            detail=f'error: error while fetching response from LLM: {str(e)}'
        )

    return HTMLResponse(content=full_html)
