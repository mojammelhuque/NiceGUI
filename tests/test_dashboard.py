from nicegui import ui
from nicegui.testing import User


async def test_task_workflow(user: User) -> None:
    await user.open('/')
    await user.should_see('2 of 5 tasks complete')
    user.find('New task').click()
    user.find('Add task').click()
    await user.should_see('Enter a task name first.')
    user.find('Task name').type('Write the project notes')
    user.find('Add task').click()
    await user.should_see('Write the project notes')
    await user.should_see('2 of 6 tasks complete')

    search = next(e for e in user.find(ui.input).elements if e.props.get('placeholder') == 'Search tasks')
    with user:
        search.set_value('project notes')
    await user.should_see('1 of 6 tasks')
    user.find(ui.checkbox).click()
    await user.should_see('3 of 6 tasks complete')
    user.find('Export CSV').click()
    response = await user.download.next()
    assert 'Write the project notes,Development,Complete' in response.text

    # Target the one delete button left by the search filter.
    user.find('close').click()
    await user.should_see('No tasks here yet.')
    await user.should_see('2 of 5 tasks complete')


async def test_reload_restores_demo(user: User) -> None:
    await user.open('/')
    user.find(ui.checkbox).click()
    await user.should_see('1 of 5 tasks complete')
    await user.open('/')
    await user.should_see('2 of 5 tasks complete')
