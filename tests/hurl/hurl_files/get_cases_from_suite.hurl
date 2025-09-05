GET {{TESTRAIL_BASE_URL}}/index.php?/api/v2/get_cases/{{fx_desk_id}}&suite_id={{SUITE_ID}}
Content-Type: application/json
HTTP 200
[Asserts]
jsonpath "$.size" == 46
jsonpath "$.cases[0].id" == 127238
jsonpath "$.cases[0].title" startsWith "Verify that the Find"
jsonpath "$.cases[0].custom_automation_status" == 2
jsonpath "$.cases[0].custom_automation_coverage" == 1
