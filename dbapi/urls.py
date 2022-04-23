from django.urls import path
from .views import DBAPI, searchSQL, diveSearch

urlpatterns = [
    path("fetch/<str:action>/<str:model>/<str:key>/<str:value>/", DBAPI.as_view(), name="fetch"),
    path("fetch/<str:action>/<str:model>/", DBAPI.as_view(), name="fetch_all"),
    path("lose/<str:action>/<str:model>/<str:key>/<str:value>/", DBAPI.as_view(), name = "delete"),
    path("fetch/<str:action>/<str:model>/<str:xkey>/", DBAPI.as_view(), name="fetch_xkey"),
    path("lend/<str:model>/", DBAPI.as_view(), name = "create"),
    path("update/<str:model/<str:key>/<str:value>/", DBAPI.as_view(), name = "update"),
    path("update/<str:model/<str:key>/", DBAPI.as_view(), name = "delete_field"),
    path("fetch/<str:action>/<str:model>/<str:key>/<str:value>/<str:xkey>/", DBAPI.as_view(), name="fetch_key"),
    path("get/<str:table>/<path:route>", searchSQL, name='searchsql'),
    path('dive/',diveSearch, name='dive_search'),
]
