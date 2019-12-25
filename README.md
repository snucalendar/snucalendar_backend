# API

## POST api/login/
``` json
{
    "email" : "email@naver.com",
    "password" : "password"

}
```

## GET api/logout/

## POST api/signup/
``` json
{
    "email" : "email@naver.com",
    "username" : "username",
    "password" : "password",
}
```
## GET api/userinfo/
``` json 
{
    "email" : "email@naver.com",
    "username" : "username"
}
```

## GET /api/calendar/<int:year>/<int:month>/
``` json
[
    {
        "year" : 2019,
        "month" : 12,
        "date" : 1,
        "events" : ["list of events"]
    },
    {
        "year" : 2019,
        "month" : 12,
        "date" : 2,
        "events" : ["list of events"]
    },
    
]
```
