GET {{BUGZILLA_BASE_URL}}/rest/bug/{{bug_id}}
HTTP 200
[Asserts]
jsonpath "$.bugs[0].creator_detail.nick" == "benchatt"
