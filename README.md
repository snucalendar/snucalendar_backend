# API

## POST api/login
##### Request
``` json
{
    "email" : "email@naver.com",
    "password" : "password"

}
```

## GET api/logout
##### no json

## POST api/signup
##### Request
``` json
{
    "email" : "email@naver.com",
    "username" : "username",
    "password" : "password",
}
```
## GET api/userinfo
##### Response
``` json 
{
    "email" : "email@naver.com",
    "username" : "username"
}
```

## GET /api/calendar/<int:year>/<int:month>
##### Response
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

## GET /api/calendar/<int:year>/<int:month>/<int:date>
##### Response
``` json
{
    "year" : 2019,
    "month" : 12,
    "date" : 25,
    "events" : ["list of events"]
}
```

## POST /api/events
##### Request
``` json
{
    "title" : "title",
    "content" : "content of event",
    "author" : "username of author"
    "date" : "date of event(format : ‘YYYY/MM/DD’)",
    "time" : "specific time of event(format : ‘HH::MM:SS’)",
    "event_type" : "festival",
    "interest" : [관심을 표시한 사람들 id],
    "list" : ["참여한 사람들 id"]
}
```

## GET /api/events/<int:id>
##### Response
``` json
{
    "title" : "title of event",
    "content" : "content",
    "date" : "date of event",
    "time" : "specific time of the event",
    "event_type" : "festival",
    "like" : "좋아요 개수"
}
```

## PUT /api/events/<int:id>
##### Request
``` json
{
    "title" : "changed title of event",
    "content" : "changed content",
    "date" : "changed date of event",
    "time" : "changed specific time of the event",
    "event_type" : "changed festival",
    "like" : "좋아요 개수"
}
```

## DELETE /api/events/<int:id>
##### no json

## POST /api/events/<int:id>/participate
##### Request
``` json
{
    "type" : "'participate' or 'interested' or null"
}
```

## GET /api/search/<str:keyword>
##### Response
``` json
{
    "events" : ["list of events"]
}
```

## POST /api/like/<int:id>
##### Request
``` json
{}
```
현재 좋아요 <-> 취소 상태를 toggle

## GET /api/like/<int:id>
##### Request
좋아요 개수를 받아옴

## GET /api/myevents
##### Response
``` json
{
    "participated_events" : [],
    "interested_events" : []
}
```
