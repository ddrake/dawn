"""
Add the standard set of tasks to the database

mpy shell
from hours.scripts import add_tasks
add_tasks.create_tasks()
"""
from hours.models import Task, TaskTranslation


def create_tasks():
    t1 = Task.objects.create(name='Grant writing & procurement')
    t2 = Task.objects.create(name="warehouse, shipment packaging")
    t3 = Task.objects.create(name="donations procurement")
    t4 = Task.objects.create(name="social media")
    t5 = Task.objects.create(name="networking")
    t6 = Task.objects.create(name="finding funding sources")
    t7 = Task.objects.create(name="administrative tasks")
    t8 = Task.objects.create(name="shipping")
    t9 = Task.objects.create(name="events")
    t10 = Task.objects.create(
        name="writing (blogs, newsletters, reports, letters, etc...)")
    t11 = Task.objects.create(name="other")

    TaskTranslation.objects.create(
        task_id=t1.pk,
        name='Grant writing & procurement',
        language='en-us')
    TaskTranslation.objects.create(
        task_id=t1.pk,
        name='Написання грантів',
        language='uk')

    TaskTranslation.objects.create(
        task_id=t2.pk,
        name="warehouse, shipment packaging",
        language='en-us')
    TaskTranslation.objects.create(
        task_id=t2.pk,
        name="склад, пакування для відправки",
        language='uk')

    TaskTranslation.objects.create(
        task_id=t3.pk,
        name="donations procurement",
        language='en-us')
    TaskTranslation.objects.create(
        task_id=t3.pk,
        name="участь у зборі донатів( пожертвувань)",
        language='uk')

    TaskTranslation.objects.create(
        task_id=t4.pk,
        name="social media",
        language='en-us')
    TaskTranslation.objects.create(
        task_id=t4.pk,
        name="соціальні мережі",
        language='uk')

    TaskTranslation.objects.create(
        task_id=t5.pk,
        name="networking",
        language='en-us')
    TaskTranslation.objects.create(
        task_id=t5.pk,
        name="будування зв'язків та відносин",
        language='uk')

    TaskTranslation.objects.create(
        task_id=t6.pk,
        name="finding funding sources",
        language='en-us')
    TaskTranslation.objects.create(
        task_id=t6.pk,
        name="пошук джерел фінансування",
        language='uk')

    TaskTranslation.objects.create(
        task_id=t7.pk,
        name="administrative tasks",
        language='en-us')
    TaskTranslation.objects.create(
        task_id=t7.pk,
        name="адміністративні завдання",
        language='uk')

    TaskTranslation.objects.create(
        task_id=t8.pk,
        name="shipping",
        language='en-us')
    TaskTranslation.objects.create(
        task_id=t8.pk,
        name="відправка",
        language='uk')

    TaskTranslation.objects.create(
        task_id=t9.pk,
        name="events",
        language='en-us')
    TaskTranslation.objects.create(
        task_id=t9.pk,
        name="події/заходи",
        language='uk')

    TaskTranslation.objects.create(
        task_id=t10.pk,
        name="writing (blogs, newsletters, reports, letters, etc...)",
        language='en-us')
    TaskTranslation.objects.create(
        task_id=t10.pk,
        name="написання (блогів, газет, звітів, листів і т.д.)",
        language='uk')

    TaskTranslation.objects.create(
        task_id=t11.pk,
        name="other",
        language='en-us')
    TaskTranslation.objects.create(
        task_id=t11.pk,
        name="iнше",
        language='uk')
