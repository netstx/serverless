# What's My IP

This lambda function parses HTTP headers from a request to an API (AWS API Gateway), then responds with the source IP address of the request using the X-Forwaded-For HTTP header data.

Based on http://checkip.dyndns.org/ and many other similar services.

It's possible to return different responses based on the URL path (.../path1, .../path2) by using the rawPath dict given by the Lambda event data. Additional routes pointing to this function are required in this case. You could also parse other data (user-agent, port, protocol, etc) and return those instead.

If path is '/' then it will respond with the entire contents of the HTTP request (the Lambda event data).
