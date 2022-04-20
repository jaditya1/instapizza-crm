from django.urls import path
from ZapioApi.Api.BrandApi.managers.usertype.usertype_create_update import UserTypeCreationUpdation
from ZapioApi.Api.BrandApi.managers.usertype.listing import UserTypeListing
from ZapioApi.Api.BrandApi.managers.usertype.activelisting import UserTypeActiveListing
from ZapioApi.Api.BrandApi.managers.usertype.retrieve import UserTypeRetrieval
from ZapioApi.Api.BrandApi.managers.usertype.action import UserTypeAction
from ZapioApi.Api.BrandApi.managers.profile.manager_create_update import ManagerCreationUpdation
from ZapioApi.Api.BrandApi.managers.profile.listing import ManagersListing
from ZapioApi.Api.BrandApi.managers.profile.retrieve import ManagerRetrieval
from ZapioApi.Api.BrandApi.managers.profile.action import ManagerAction

from ZapioApi.Api.BrandApi.managers.permission.module_list import ModuleListing
from ZapioApi.Api.BrandApi.managers.permission.mainroute_list import MainRouteListing
from ZapioApi.Api.BrandApi.managers.permission.route_list import RouteListing
from ZapioApi.Api.BrandApi.managers.permission.sub_route_list import SubRouteListing

urlpatterns = [

	path('listing/usertype/',UserTypeListing.as_view()),
	path('activelisting/usertype/',UserTypeActiveListing.as_view()),
	path('retrieval/usertype/',UserTypeRetrieval.as_view()),
	path('createupdate/usertype/',UserTypeCreationUpdation.as_view()),
	path('action/usertype/',UserTypeAction.as_view()),

	path('listing/profile/',ManagersListing.as_view()),
	path('retrieval/profile/',ManagerRetrieval.as_view()),
	path('createupdate/profile/',ManagerCreationUpdation.as_view()),
	path('action/profile/',ManagerAction.as_view()),

	path('listing/Module/',ModuleListing.as_view()),
	path('listing/MainRoute/',MainRouteListing.as_view()),
	path('listing/Route/',RouteListing.as_view()),
	path('listing/SubRoute/',SubRouteListing.as_view()),
]