def test_drag_example(page):
    page.goto("https://seleniumbase.io/other/drag_and_drop")

    drag_img = page.locator("#drag1")
    drop_1 = page.locator("#div1")
    drop_2 = page.locator("#div2")
    drag_img.drag_to(drop_1)
    drag_img.drag_to(drop_2)
