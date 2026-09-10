from aiohttp import web

from ad_14_tasks import celery_app, generate_report


async def submit_report(request: web.Request) -> web.Response:
    """POST /reports - przyjmuje zadanie generowania raportu, zwraca task_id."""
    data = await request.json()
    report_id = data.get("report_id")

    if report_id is None:
        return web.json_response({"error": "Wymagane pole: report_id"}, status=400)

    task = generate_report.delay(report_id)

    return web.json_response({"task_id": task.id, "status": "queued"}, status=202)


async def get_report_status(request: web.Request) -> web.Response:
    """GET /reports/{task_id} - sprawdza status zadania."""
    task_id = request.match_info["task_id"]
    task_result = celery_app.AsyncResult(task_id)

    response_data = {
        "task_id": task_id,
        "status": task_result.status,
    }

    if task_result.ready():
        response_data["result"] = task_result.result

    return web.json_response(response_data)


def create_app() -> web.Application:
    app = web.Application()
    app.router.add_post("/reports", submit_report)
    app.router.add_get("/reports/{task_id}", get_report_status)
    return app


if __name__ == "__main__":
    web.run_app(create_app(), host="0.0.0.0", port=8000)