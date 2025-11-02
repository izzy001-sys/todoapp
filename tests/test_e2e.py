import pytest
from playwright.sync_api import Page, expect


@pytest.fixture(scope="module")
def base_url():
    return "http://127.0.0.1:8000"


def test_signup_and_create_todo(page: Page, base_url):
    # Go to signup page
    page.goto(f"{base_url}/signup")
    
    # Fill signup form
    page.fill('input[name="username"]', "e2etestuser")
    page.fill('input[name="email"]', "e2etest@example.com")
    page.fill('input[name="password"]', "testpass123")
    
    # Submit form
    page.click('button[type="submit"]')
    
    # Should redirect to home
    expect(page).to_have_url(f"{base_url}/")
    
    # Should see welcome message
    expect(page.locator("text=Welcome, e2etestuser")).to_be_visible()
    
    # Create a todo
    page.fill('#todo-title', "My First Todo")
    page.fill('#todo-description', "This is a test todo")
    page.click('#todo-form button[type="submit"]')
    
    # Should see the todo in the list
    expect(page.locator("text=My First Todo")).to_be_visible()
    expect(page.locator("text=This is a test todo")).to_be_visible()


def test_login(page: Page, base_url):
    # Go to login page
    page.goto(f"{base_url}/login")
    
    # Fill login form
    page.fill('input[name="username"]', "e2etestuser")
    page.fill('input[name="password"]', "testpass123")
    
    # Submit form
    page.click('button[type="submit"]')
    
    # Should redirect to home
    expect(page).to_have_url(f"{base_url}/")
    
    # Should see welcome message
    expect(page.locator("text=Welcome, e2etestuser")).to_be_visible()


def test_todo_interactions(page: Page, base_url):
    # First login (assuming user exists from previous test)
    page.goto(f"{base_url}/login")
    page.fill('input[name="username"]', "e2etestuser")
    page.fill('input[name="password"]', "testpass123")
    page.click('button[type="submit"]')
    
    # Wait for home page
    expect(page).to_have_url(f"{base_url}/")
    
    # Create a todo if none exist
    todo_count = page.locator(".todo-item").count()
    if todo_count == 0:
        page.fill('#todo-title', "Todo to Complete")
        page.click('#todo-form button[type="submit"]')
        expect(page.locator("text=Todo to Complete")).to_be_visible()
    
    # Wait a bit for todos to load
    page.wait_for_timeout(1000)
    
    # Toggle checkbox if it exists
    checkbox = page.locator('.todo-checkbox').first
    if checkbox.count() > 0:
        checkbox.check()
        # Verify todo is marked as completed (strikethrough)
        expect(page.locator('.todo-title.completed').first).to_be_visible()
    
    # Delete todo if button exists
    delete_btn = page.locator('.delete-btn').first
    if delete_btn.count() > 0:
        page.on("dialog", lambda dialog: dialog.accept())  # Handle confirm dialog
        delete_btn.click()
        # Wait for deletion
        page.wait_for_timeout(500)

