from Orders.models import Order
from Product.models import KotSteps, Addons, Variant
from urbanpiper.models import ProductSync
import re

def kot_process_data(order_id):
	record = Order.objects.filter(id=order_id)[0]
	c_id = record.Company_id
	order_desc = record.order_description
	for i in order_desc:
		kot = {"make_table":{},"cut_table":{}}
		kot["make_table"]["description"] = []
		kot["make_table"]["crust"] = []
		kot["make_table"]["base_sauce"] = []
		kot["make_table"]["toppings"] = []
		kot["make_table"]["additional_toppings"] = []
		kot["make_table"]["cheese"] = []
		kot["make_table"]["extra_cheese"] = []
		kot["cut_table"]["sauces_on_top"] = []
		kot["cut_table"]["garnishes"] = []
		kot["cut_table"]["add_ons"] = []
		kot["cut_table"]["seasoning"] = []
		kot["cut_table"]["fried_filling"] = []
		if "kot_desc" in i:
			i["kot_desc"] = kot
		else:
			i["kot_desc"] = kot
		if "final_product_id" in i:
			i["id"] = ProductSync.objects.filter(id=i["final_product_id"])[0].product_id
			i["v_id"] = ProductSync.objects.filter(id=i["final_product_id"])[0].variant_id
		else:
			pass
		if len(i["add_ons"]) == 0:
			pass
		else:
			for j in i["add_ons"]:
				if "final_addon_id" in j:
					j["addon_id"] = j["final_addon_id"]
					del j["final_addon_id"]
				else:
					pass
		if "size" in i and "final_product_id" not in i:
			v_record = Variant.objects.filter(variant=i["size"],Company=c_id)
			if v_record.count() != 0:
				i["v_id"] = v_record[0].id
			else:
				i["v_id"] = None
		else:
			pass
		kot_record = KotSteps.objects.filter(product=i["id"])
		make_description_record = kot_record.filter(kot_category="0", step_name="0")
		if make_description_record.count()!=0:
			make_des = make_description_record[0].kot_desc
			final_make_des = make_des.split(',')
			i["kot_desc"]["make_table"]["description"] = final_make_des
		else:
			pass
		make_crust_record = kot_record.filter(kot_category="0", step_name="1")
		make_crust_record = make_crust_record.filter(variant=i["v_id"])
		if make_crust_record.count()!=0:
			make_crust = make_crust_record[0].kot_desc
			final_make_crust = make_crust.split(',')
			i["kot_desc"]["make_table"]["crust"] = final_make_crust
		else:
			pass
		make_base_sauce_record = kot_record.filter(kot_category="0", step_name="2")
		if make_base_sauce_record.count() != 0:
			make_base_sauce = make_base_sauce_record[0].kot_desc
			final_make_base_sauce = make_base_sauce.split(',')
			i["kot_desc"]["make_table"]["base_sauce"] = final_make_base_sauce
		else:
			pass
		make_toppings_record = kot_record.filter(kot_category="0", step_name="3")
		if make_toppings_record.count() != 0:
			make_toppings = make_toppings_record[0].kot_desc
			final_make_toppings = make_toppings.split(',')
			i["kot_desc"]["make_table"]["toppings"] = final_make_toppings
		else:
			pass 
		make_cheese_record = kot_record.filter(kot_category="0", step_name="5")
		if make_cheese_record.count() != 0:
			make_cheese = make_cheese_record[0].kot_desc
			final_make_cheese = make_cheese.split(',')
			i["kot_desc"]["make_table"]["cheese"] = final_make_cheese
		else:
			pass
		cut_sauce_on_top_record = kot_record.filter(kot_category="1", step_name="7")
		if cut_sauce_on_top_record.count()!= 0:
			cut_sauce_on_top = cut_sauce_on_top_record[0].kot_desc
			final_cut_sauce_on_top = cut_sauce_on_top.split(',')
			i["kot_desc"]["cut_table"]["sauces_on_top"] = final_cut_sauce_on_top
		else:
			pass
		cut_garnish_record = kot_record.filter(kot_category="1", step_name="8")
		if cut_garnish_record.count() != 0:
			cut_garnish = cut_garnish_record[0].kot_desc
			final_cut_garnish = cut_garnish.split(',')
			i["kot_desc"]["cut_table"]["garnishes"] = final_cut_garnish
		else:
			pass

		cut_garnish_record = kot_record.filter(kot_category="1", step_name="8")
		if cut_garnish_record.count() != 0:
			cut_garnish = cut_garnish_record[0].kot_desc
			final_cut_garnish = cut_garnish.split(',')
			i["kot_desc"]["cut_table"]["garnishes"] = final_cut_garnish
		else:
			pass

		cut_garnish_record = kot_record.filter(kot_category="1", step_name="8")
		if cut_garnish_record.count() != 0:
			cut_garnish = cut_garnish_record[0].kot_desc
			final_cut_garnish = cut_garnish.split(',')
			i["kot_desc"]["cut_table"]["garnishes"] = final_cut_garnish
		else:
			pass

		cut_seasoning_record = kot_record.filter(kot_category="1", step_name="11")
		if cut_seasoning_record.count() != 0:
			cut_seasoning = cut_seasoning_record[0].kot_desc
			final_cut_seasoning = cut_seasoning.split(',')
			i["kot_desc"]["cut_table"]["seasoning"] = final_cut_seasoning
		else:
			pass

		add_ons_record = kot_record.filter(kot_category="1", step_name="9")
		if add_ons_record.count() != 0:
			cut_addons = add_ons_record[0].kot_desc
			final_cut_addons = cut_addons.split(',')
			i["kot_desc"]["cut_table"]["add_ons"] = final_cut_addons
		else:
			pass

		fried_filling_record = kot_record.filter(kot_category="1", step_name="10")
		if fried_filling_record.count() != 0:
			cut_fried_filling = fried_filling_record[0].kot_desc
			final_fried_filling = cut_fried_filling.split(',')
			i["kot_desc"]["cut_table"]["fried_filling"] = final_fried_filling
		else:
			pass

		if len(i["add_ons"]) == 0:
			pass
		else:
			for k in i["add_ons"]:
				to_process = 0
				addon_record = Addons.objects.filter(id=k["addon_id"])
				if addon_record.count()!=0:
					to_process = 1
					addon_grp_type = addon_record[0].addon_group.addon_grp_type
					if addon_grp_type != None:
						pass
					else:
						addon_grp_type = "10"
				else:
					pass
				add_on_name = addon_record[0].name
				if to_process == 1:
					if addon_grp_type == "0":
						i["kot_desc"]["make_table"]["crust"].append(add_on_name)
					else:
						pass
					if addon_grp_type == "1":
						i["kot_desc"]["cut_table"]["sauces_on_top"].append(add_on_name)
					else:
						pass
					if addon_grp_type == "2":
						if re.search("extra", add_on_name, re.IGNORECASE):
							final_addon_name = add_on_name.replace('Extra','')
							final_addon_name = final_addon_name.replace('extra','')
							i["kot_desc"]["make_table"]["cheese"].append(final_addon_name)
							i["kot_desc"]["make_table"]["extra_cheese"].append(final_addon_name)
						else:
							i["kot_desc"]["make_table"]["cheese"].append(add_on_name)
					else:
						pass
					if addon_grp_type == "3":
						i["kot_desc"]["make_table"]["additional_toppings"].append(add_on_name)
					else:
						pass
					if addon_grp_type == "4":
						i["kot_desc"]["cut_table"]["add_ons"].append(add_on_name)
					else:
						pass
				else:
					pass
	return order_desc