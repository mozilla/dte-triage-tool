GET {{BUGZILLA_BASE_URL}}/rest/bug
[QueryStringParams]
summary: Create pref to enable Firefox Refresh testing
HTTP 200
[Asserts]
jsonpath "$.bugs[0].id" == 1989465
