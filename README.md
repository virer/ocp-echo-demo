# OCP-ECHO-DEMO

A little python Flask API demo with caching dict

### Add some
```
$ curl -H 'Content-Type: application/json' -X POST '{ "environment": "dev", "service":"foo","version":"1.2" }' http://127.0.0.1:8080/api/version
$ curl -H 'Content-Type: application/json' -X POST '{ "environment": "test", "service":"foo","version":"1.1" }' http://127.0.0.1:8080/api/version
```

### Check the content
```
$ curl http://127.0.0.1:8080/api/version
{"version":{"foo":{"dev":"1.2","integration":"NoVersion","production":"NoVersion","test":"1.1"}}}
```

### Clear the cache
```
curl -X DELETE http://127.0.0.1:8080/api/cache
```

Author: S.CAPS
Date: 02/2021