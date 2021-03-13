import json

def lambda_handler(event, context):

  response = {
    "statusCode": 200,
    "headers": {
      "Content-Type": "text/plain;"
    },
    "isBase64Encoded": False
  }

sourceip_list = event['headers']['x-forwarded-for'].split(',')

  if event['rawPath'] == '/whatsmyip':
    if sourceip_list:
      sourceip = str(sourceip_list[0])
      response['body']=sourceip
      print("/whatsmyip request from: " + sourceip)
    else:
      response['body']='0.0.0.0'
    return response
    
  if event['rawPath'] == '/pfsense':
    if sourceip_list:
      sourceip = str(sourceip_list[0])
      response['body']="Current IP Address: " + sourceip
      print("/pfsense request from: " + sourceip)
    else:
      response['body']="Current IP Address: 0.0.0.0"
    return response
    
  response['body'] = json.dumps(event, indent=2)
  print("Root path request")
  return response
