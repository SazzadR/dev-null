import asyncio
import pprint
import random
import time

accounting_database = {
    "invoices": [],
    "amount": 0,
}

invoices = {
    "invoice_01": {"amount": 100, "wait_time": 1},
    "invoice_02": {"amount": 200, "wait_time": 1},
    "invoice_03": {"amount": 300, "wait_time": 1},
    "invoice_04": {"amount": 400, "wait_time": 1},
    "invoice_05": {"amount": 500, "wait_time": 1},
}


lock = asyncio.Lock()


async def get_invoice_async_with_lock(invoice_name):
        invoice = invoices[invoice_name]

        await asyncio.sleep(invoice["wait_time"])

        accounting_database["invoices"].append(
            {"name": invoice_name, "amount": invoice["amount"]}
        )

        async with lock:
            current_amount = accounting_database["amount"]
            await asyncio.sleep(random.uniform(0.01, 0.1))
            accounting_database["amount"] = current_amount + invoice["amount"]


async def main_async_with_lock():
    start = time.perf_counter()

    tasks = []
    async with asyncio.TaskGroup() as task_group:
        for invoice_name, invoice in invoices.items():
            task = task_group.create_task(get_invoice_async_with_lock(invoice_name))
            tasks.append(task)

    pprint.pprint(accounting_database)
    print(f"Took: {(time.perf_counter() - start):.2f} seconds.")


async def get_invoice_async(invoice_name):
    invoice = invoices[invoice_name]

    await asyncio.sleep(invoice["wait_time"])

    accounting_database["invoices"].append(
        {"name": invoice_name, "amount": invoice["amount"]}
    )

    current_amount = accounting_database["amount"]

    await asyncio.sleep(random.uniform(0.01, 0.1))

    accounting_database["amount"] = current_amount + invoice["amount"]


async def main_async():
    start = time.perf_counter()

    tasks = []
    async with asyncio.TaskGroup() as task_group:
        for invoice_name, invoice in invoices.items():
            task = task_group.create_task(get_invoice_async(invoice_name))
            tasks.append(task)

    pprint.pprint(accounting_database)
    print(f"Took: {(time.perf_counter() - start):.2f} seconds.")


def get_invoice_sync(invoice_name):
    invoice = invoices[invoice_name]

    time.sleep(invoice["wait_time"])

    accounting_database["invoices"].append(
        {"name": invoice_name, "amount": invoice["amount"]}
    )

    accounting_database["amount"] += invoice["amount"]


def main_sync():
    start = time.perf_counter()

    for invoice_name, invoice in invoices.items():
        get_invoice_sync(invoice_name)

    pprint.pprint(accounting_database)
    print(f"Took: {(time.perf_counter() - start):.2f} seconds.")


if __name__ == "__main__":
    # main_sync()
    # asyncio.run(main_async())
    asyncio.run(main_async_with_lock())
