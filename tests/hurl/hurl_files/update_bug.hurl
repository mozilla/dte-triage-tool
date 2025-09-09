PUT {{BUGZILLA_BASE_URL}}/rest/bug/{{BUG_ID}}?api_key={{BUGZILLA_API_KEY}}
{
    "ids": [{{BUG_ID}}],
    "blocks": {
        "add": [{{BLOCKED_BUG_ID}}]
    }
}

