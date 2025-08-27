GET {{BASE_URL}}/index.php?/api/v2/get_suites/{{fx_desk_id}}
Content-Type: application/json
HTTP 200
[Asserts]
jsonpath "$.size" > 50
jsonpath "$.suites[0].id" exists
jsonpath "$.suites[0].name" exists
jsonpath "$.suites[0].description" exists
jsonpath "$.suites[0].url" exists
