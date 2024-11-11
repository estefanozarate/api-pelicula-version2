import boto3
import uuid
import json

def lambda_handler(event, context):
    try:
        # Extracción de datos del evento
        tenant_id = event['body']['tenant_id']
        pelicula_datos = event['body']['pelicula_datos']
        nombre_tabla = "TABLAPELICULA"  # Nombre de la tabla fijo
        uuidv4 = str(uuid.uuid4())

        # Creación de datos de la película
        pelicula = {
            'tenant_id': tenant_id,
            'uuid': uuidv4,
            'pelicula_datos': pelicula_datos
        }

        # Inserción en DynamoDB
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(nombre_tabla)
        response = table.put_item(Item=pelicula)

        # Log de éxito en formato JSON
        log_info = {
            "tipo": "INFO",
            "log_datos": {
                "mensaje": "Película creada correctamente",
                "pelicula": pelicula,
                "response": response
            }
        }
        print(json.dumps(log_info))  # Imprime el log en formato JSON

        return {
            'statusCode': 200,
            'pelicula': pelicula,
            'response': response
        }
    
    except Exception as e:
        # Log de error en formato JSON
        log_error = {
            "tipo": "ERROR",
            "log_datos": {
                "mensaje": "Error al crear la película",
                "error": str(e)
            }
        }
        print(json.dumps(log_error))  # Imprime el log de error en formato JSON

        return {
            'statusCode': 500,
            'error': str(e)
        }


