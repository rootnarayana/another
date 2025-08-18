import azure.functions as func
import logging

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="http_trigger1")
@app.cosmos_db_output(arg_name="outputDocument", database_name="venkat1", container_name="venkatcon1", connection="CosmosDBConnectionString[AccountKey]")
def http_trigger1(req: func.HttpRequest,outputDocument: func.Out[func.Document]) -> func.HttpResponse:
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
        logging.info(f"Adding item: {name} - {date}")
        # outputDocument.set(func.Document.from_dict({"id": name}))

        return func.HttpResponse(f"Item '{name} - {date}' added successfully.", status_code=200)

    elif operation == 'remove':
        logging.info(f"Removing item: {name} - {date}")
        return func.HttpResponse(f"Item '{name} - {date}' removed successfully.", status_code=200)

    else:
        return func.HttpResponse("Invalid operation. Use 'add' or 'remove'.", status_code=400)