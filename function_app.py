import azure.functions as func
import logging
import uuid

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="http_trigger1")
# @app.cosmos_db_output(
#     arg_name="outputDocument",
#     database_name="venkat1",
#     container_name="venkatcon1",
#     connection="connectionstring"
# )outputDocument: func.Out[func.Document]
@app.queue_output(arg_name="msg", queue_name="queueven", connection="AzureWebJobsStorage")
def http_trigger1(req: func.HttpRequest, msg: func.Out [func.QueueMessage]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse("Invalid JSON", status_code=400)

    name = req_body.get('name')
    date = req_body.get('date')
    operation = req_body.get('operation')

    if not name or not date or not operation:
        return func.HttpResponse("Missing name, date, or operation field.", status_code=400)

    if operation == 'add': 
        msg.set(name)
        logging.info(f"Adding item: {name} - {date}")

        return func.HttpResponse(f"Item '{name} - {date}' added successfully.", status_code=200)

    elif operation == 'remove':
        logging.info(f"Remove requested: {name} - {date}")
        # ⚠️ Cosmos DB binding does not support delete directly.
        # You must use Cosmos SDK here if you really want to delete.
        return func.HttpResponse("Remove operation not yet implemented.", status_code=501)

    else:
        return func.HttpResponse("Invalid operation. Use 'add' or 'remove'.", status_code=400)
