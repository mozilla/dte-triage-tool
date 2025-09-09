GET {{BUGZILLA_BASE_URL}}/rest/bug/{{bug_id}}?api_key={{BUGZILLA_API_KEY}}
HTTP 200
[Asserts]
jsonpath "$.bugs[0].creator_detail.nick" == "benchatt"
