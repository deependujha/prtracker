Nice, this is exactly the right time to add this — macros + a few power features will save you from messy templates later.

Here’s your upgraded version 👇

______________________________________________________________________

# ⚡ FastAPI + Jinja2 Quick Reference

## 1. Setup Templates

```python
from pathlib import Path
from fastapi.templating import Jinja2Templates

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / "ui"

templates = Jinja2Templates(directory=TEMPLATES_DIR)
```

______________________________________________________________________

## 2. Render Templates

```python
from fastapi import APIRouter, Request

router = APIRouter()

@router.get("/")
def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )
```

### With data

```python
@router.get("/page")
def page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="page.html",
        context={"key": "value"}
    )
```

______________________________________________________________________

## 3. Full HTML vs Partial

- **Full page** → complete document
- **Partial** → reusable fragments

```html
<div>partial content</div>
```

______________________________________________________________________

## 4. Access Data

```html
<p>{{ key }}</p>
<p>{{ key | default("N/A") }}</p>
```

______________________________________________________________________

## 5. Control Flow

### Condition

```html
{% if key == "value" %}
  <p>match</p>
{% endif %}
```

### Loop

```html
{% for item in items %}
  <li>{{ item }}</li>
{% endfor %}
```

______________________________________________________________________

## 6. Template Inheritance (must-use)

### `base.html`

```html
<!DOCTYPE html>
<html>
<head>
  <title>{% block title %}App{% endblock %}</title>
</head>
<body>
  {% block content %}{% endblock %}
</body>
</html>
```

### `index.html`

```html
{% extends "base.html" %}

{% block content %}
  <h1>Welcome</h1>
{% endblock %}
```

______________________________________________________________________

## 7. Macros (reusable UI components)

> Think: functions for HTML

### Define macro (`macros.html`)

```html
{% macro badge(text, color="gray") %}
  <span class="badge badge-{{ color }}">
    {{ text }}
  </span>
{% endmacro %}
```

### Use macro

```html
{% from "macros.html" import badge %}

{{ badge("Open", "green") }}
{{ badge("Closed", "red") }}
```

### With blocks (advanced)

```html
{% macro card(title) %}
  <div class="card">
    <h2>{{ title }}</h2>
    <div>
      {{ caller() }}
    </div>
  </div>
{% endmacro %}

{% call card("My Card") %}
  <p>Inner content</p>
{% endcall %}
```

> If you’re repeating markup → extract a macro. No excuses.

______________________________________________________________________

## 8. Includes (simpler reuse than macros)

```html
{% include "partials/header.html" %}
```

> Use includes for static chunks, macros for dynamic components.

______________________________________________________________________

## 9. Filters (built-in helpers)

```html
{{ name | upper }}
{{ items | length }}
{{ text | truncate(50) }}
{{ value | default("N/A") }}
```

### Chaining

```html
{{ name | default("unknown") | upper }}
```

______________________________________________________________________

## 10. Set Variables

```html
{% set total = items | length %}
<p>Total: {{ total }}</p>
```

______________________________________________________________________

## 11. Conditions You’ll Actually Use

```html
{% if items %}
  <!-- not empty -->
{% endif %}

{% if user is defined %}
  {{ user.name }}
{% endif %}
```

______________________________________________________________________

## 12. Recommended Structure

```
project/
├── server/
├── ui/
│   ├── base.html
│   ├── index.html
│   ├── macros.html
│   └── partials/
```

______________________________________________________________________

## 13. Common Gotchas

- `request` is required
- Missing variables fail silently
- Don’t put business logic in templates
- Macros ≠ includes (don’t mix mental models)
