from django.urls import path
from ZapioApi.Api.urbanpiper.listing.outlet import UrbanOutletListing, UnInitiatedOutletListing
from ZapioApi.Api.urbanpiper.listing.synced_outlet import SyncedOutletListing
from ZapioApi.Api.urbanpiper.attach import UrbanOutletAttach
from ZapioApi.Api.urbanpiper.sync.outlet import OutletToSync
from ZapioApi.Api.urbanpiper.action.action import OutletAction
from ZapioApi.Api.urbanpiper.menu.cat_attach import CatAttach
from ZapioApi.Api.urbanpiper.menu.product_attach import ProductAttach
from ZapioApi.Api.urbanpiper.listing.synced_menu import SyncedProduct, SyncedCat, SyncedSubCat

from ZapioApi.Api.urbanpiper.sync.menu import UniversalSync, SwiggySync, ZomatoSync
from ZapioApi.Api.urbanpiper.sync.master_flush import MasterFlush

from ZapioApi.Api.urbanpiper.menu.cat_retrieve import CatRetrieval
from ZapioApi.Api.urbanpiper.menu.cat_priority import SetPriority

from ZapioApi.Api.urbanpiper.menu.sub_cat_retrieve import SubCatRetrieval
from ZapioApi.Api.urbanpiper.menu.subcat_priority import SetSubCatPriority



urlpatterns = [

	path('listing/outlet/',UrbanOutletListing.as_view()),
	path('listing/not_initiated_outlet/',UnInitiatedOutletListing.as_view()),
	path('listing/synced_outlet/',SyncedOutletListing.as_view()),
	path('listing/category/',SyncedCat.as_view()),
	path('listing/subcategory/',SyncedSubCat.as_view()),
	path('listing/product/',SyncedProduct.as_view()),

	path('attach/outlet/',UrbanOutletAttach.as_view()),
	path('attach/category/',CatAttach.as_view()),
	path('attach/products/',ProductAttach.as_view()),
	path('retrieve/category/', CatRetrieval.as_view()),
	path('category/SetPriority/', SetPriority.as_view()),
	path('retrieve/subcategory/', SubCatRetrieval.as_view()),
	path('category/SetSubCatPriority/', SetSubCatPriority.as_view()),

	path('sync/outlet/',OutletToSync.as_view()),
	path('action/outlet/',OutletAction.as_view()),

	path('MasterFlush/',MasterFlush.as_view()),

	path('UniversalSync/',UniversalSync.as_view()),
	path('SwiggySync/',SwiggySync.as_view()),
	path('ZomatoSync/',ZomatoSync.as_view()),

]