"""Run with `python main.py`, then open http://localhost:8080."""

import csv
import io
from dataclasses import dataclass

from nicegui import ui


@dataclass
class Task:
    title: str
    category: str
    done: bool = False


@ui.page('/')
def dashboard() -> None:
    # Keeping state inside the page gives each visitor an independent demo.
    tasks = [
        Task('Sketch the dashboard layout', 'Design', True),
        Task('Build the first NiceGUI page', 'Development', True),
        Task('Explore interactive components', 'Learning'),
        Task('Connect a real data source', 'Development'),
        Task('Polish the finishing touches', 'Design'),
    ]
    ui.colors(primary='#6366f1', secondary='#14b8a6')
    ui.add_css('''
        body { background: #f5f6fa; color: #20243b; }
        .nicegui-content { padding: 0; }
        .panel { border: 1px solid #e8eaf2; border-radius: 18px;
                 box-shadow: 0 4px 24px #20243b04; background: white; }
        .eyebrow { font-size: 11px; letter-spacing: .16em; font-weight: 700; }
        .task-row:hover { background: #f8f9ff; }
    ''')

    with ui.header().classes('bg-white text-slate-800 border-b px-6 py-4'):
        with ui.row().classes('w-full max-w-6xl mx-auto items-center gap-3'):
            ui.icon('dashboard_customize', color='primary', size='30px')
            ui.label('Focus Desk').classes('text-xl font-bold')
            ui.space()
            ui.badge('NICEGUI PLAYGROUND', color='indigo-1', text_color='indigo-8')
            ui.button(icon='help_outline', on_click=lambda: about.open()).props('flat round').tooltip('About this demo')

    with ui.dialog() as about, ui.card().classes('max-w-md p-6'):
        ui.label('A little Python. A real interface.').classes('text-xl font-bold')
        ui.label('This sample combines layouts, events, forms, refreshable views, charts, dialogs, and downloads.')
        ui.label('Each page load starts a fresh demo. Your changes are kept only while this page is open.').classes('text-slate-500')
        ui.link('Explore NiceGUI documentation', 'https://nicegui.io/documentation', new_tab=True)
        ui.button('Got it', on_click=about.close)

    def refresh() -> None:
        summary.refresh()
        task_list.refresh()
        breakdown.refresh()

    def set_done(task: Task, value: bool) -> None:
        task.done = value
        refresh()

    def remove(task: Task) -> None:
        tasks.remove(task)
        refresh()
        ui.notify('Task removed', type='info')

    def add_task() -> None:
        value = (title.value or '').strip()
        if not value:
            ui.notify('Enter a task name first.', type='warning')
            return
        if len(value) > 120:
            ui.notify('Keep the task name to 120 characters.', type='warning')
            return
        tasks.append(Task(value, category.value))
        title.set_value('')
        new_task.close()
        refresh()
        ui.notify('Task added', type='positive')

    def export() -> None:
        output = io.StringIO(newline='')
        writer = csv.writer(output)
        writer.writerow(['Task', 'Category', 'Status'])
        for task in tasks:
            # Prefix formula-like text so spreadsheet programs treat it as text.
            safe_title = task.title
            if safe_title.lstrip().startswith(('=', '+', '-', '@')):
                safe_title = "'" + safe_title
            writer.writerow([safe_title, task.category, 'Complete' if task.done else 'Open'])
        ui.download(output.getvalue().encode('utf-8-sig'), 'focus-desk-tasks.csv')

    with ui.dialog() as new_task, ui.card().classes('w-full max-w-md p-6'):
        ui.label('Make room for your next idea').classes('text-xl font-bold')
        title = ui.input('Task name', placeholder='What would you like to do?').props('outlined maxlength=120').classes('w-full')
        title.on('keydown.enter', add_task)
        category = ui.select(['Design', 'Development', 'Learning'], value='Development', label='Category').props('outlined').classes('w-full')
        with ui.row().classes('w-full justify-end'):
            ui.button('Cancel', on_click=new_task.close).props('flat')
            ui.button('Add task', on_click=add_task)

    @ui.refreshable
    def summary() -> None:
        completed = sum(task.done for task in tasks)
        values = [
            ('Total tasks', str(len(tasks)), 'layers', 'Your ideas, organized'),
            ('In progress', str(len(tasks) - completed), 'hourglass_top', 'One step at a time'),
            ('Completed', str(completed), 'task_alt', 'Small wins add up'),
        ]
        with ui.element('div').classes('grid grid-cols-1 sm:grid-cols-3 gap-4 w-full'):
            for label, value, icon, caption in values:
                with ui.card().classes('panel p-5 gap-2'):
                    with ui.row().classes('w-full items-center justify-between'):
                        ui.label(label).classes('text-sm text-slate-500')
                        ui.icon(icon, color='primary', size='22px')
                    ui.label(value).classes('text-4xl font-bold')
                    ui.label(caption).classes('text-xs text-slate-400')

    @ui.refreshable
    def task_list() -> None:
        query = (search.value or '').casefold().strip()
        visible = [task for task in tasks if query in task.title.casefold()
                   and (status.value == 'All' or task.done == (status.value == 'Complete'))]
        if not visible:
            with ui.column().classes('w-full items-center py-12 text-slate-400'):
                ui.icon('search_off', size='40px')
                ui.label('No tasks here yet. Add one or change your filters.')
        for task in visible:
            with ui.row().classes('task-row w-full items-center flex-nowrap gap-3 py-3 border-b border-slate-100'):
                ui.checkbox(value=task.done, on_change=lambda e, t=task: set_done(t, e.value)).tooltip('Mark complete or reopen')
                with ui.column().classes('flex-1 min-w-0 gap-1'):
                    ui.label(task.title).classes('break-words ' + ('line-through text-slate-400' if task.done else 'font-medium'))
                    ui.label(task.category).classes('text-xs text-slate-400')
                ui.button(icon='close', on_click=lambda t=task: remove(t)).props('flat round dense color=grey-5').tooltip('Delete task')
        ui.label(f'{len(visible)} of {len(tasks)} tasks').classes('text-xs text-slate-400 pt-3')

    @ui.refreshable
    def breakdown() -> None:
        completed = sum(task.done for task in tasks)
        percent = round(100 * completed / len(tasks)) if tasks else 0
        ui.label('Your momentum').classes('text-lg font-bold')
        ui.label('Every finished task moves you forward.').classes('text-sm text-slate-400')
        ui.echart({
            'tooltip': {'trigger': 'item'},
            'color': ['#6366f1', '#e8eaf5'],
            'series': [{'type': 'pie', 'radius': ['70%', '88%'],
                        'label': {'show': False}, 'data': [
                            {'value': completed, 'name': 'Complete'},
                            {'value': len(tasks) - completed, 'name': 'Open'},
                        ]}],
            'graphic': [{'type': 'text', 'left': 'center', 'top': 'center',
                         'style': {'text': f'{percent}%', 'fontSize': 32,
                                   'fontWeight': 'bold', 'fill': '#20243b'}}],
        }).classes('w-full h-56')
        ui.label(f'{completed} of {len(tasks)} tasks complete').classes('self-center text-sm text-slate-500')
        ui.separator().classes('my-3')
        ui.label('TRY SOMETHING NEW').classes('eyebrow text-indigo-500')
        ui.label('Add a task, check it off, and watch this chart update instantly.').classes('text-sm text-slate-500 leading-relaxed')

    with ui.column().classes('w-full max-w-6xl mx-auto px-6 py-10 gap-7'):
        with ui.row().classes('w-full items-center justify-between gap-4'):
            with ui.column().classes('gap-2'):
                ui.label('A LITTLE CLARITY FOR YOUR DAY').classes('eyebrow text-indigo-500')
                ui.label('Good ideas start here.').classes('text-3xl sm:text-4xl font-bold tracking-tight')
                ui.label('A calm place to plan, build, and keep moving.').classes('text-slate-500')
            ui.button('New task', icon='add', on_click=new_task.open).props('unelevated no-caps').classes('px-5 py-2 rounded-xl')
        summary()
        with ui.element('div').classes('grid grid-cols-1 lg:grid-cols-3 gap-6 w-full items-start'):
            with ui.card().classes('panel lg:col-span-2 w-full p-6'):
                with ui.row().classes('w-full items-center justify-between'):
                    ui.label('Your task board').classes('text-lg font-bold')
                    ui.button('Export CSV', icon='download', on_click=export).props('flat no-caps size=sm')
                with ui.row().classes('w-full items-center gap-3'):
                    search = ui.input(placeholder='Search tasks', on_change=lambda: task_list.refresh()).props('outlined dense clearable').classes('flex-1 min-w-40')
                    with search.add_slot('prepend'):
                        ui.icon('search')
                    status = ui.select(['All', 'Open', 'Complete'], value='All', on_change=lambda: task_list.refresh()).props('outlined dense').classes('w-32')
                with ui.column().classes('w-full gap-0'):
                    task_list()
            with ui.card().classes('panel w-full p-6 gap-2'):
                breakdown()
        ui.label('Built with Python + NiceGUI · Sample data · Changes reset on page reload').classes('text-xs text-slate-400')


if __name__ == '__main__':
    ui.run(title='Focus Desk · NiceGUI', host='127.0.0.1', port=8080, show=False, reload=False)
