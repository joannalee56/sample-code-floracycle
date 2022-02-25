@app.route("/search/category")
def filter_classifieds():
    """Show all classifieds with filtered categories."""
    # Search keyword in title, description, and category tag
    search = session["search"]
    classifieds = crud.get_classified_by_keyword(search)

    search_to_return = []

    # Search filter by tag
    filtered_tags = []
    tagged_classifieds = []
    if request.args.getlist("tag_id"):
        lst_of_tag_ids = request.args.getlist("tag_id")
        for id in lst_of_tag_ids:
            tag_classifieds = crud.get_classified_by_tag(id)
            tagged_classifieds += tag_classifieds
        for tagged in tagged_classifieds:
            if(tagged in classifieds):
                filtered_tags.append(tagged)
    else:
        filtered_tags = classifieds
    filtered_tags = set(filtered_tags)

    # Search filter by cost type
    if request.args.get("cost-type"):
        cost_type = request.args.get("cost-type")
        filtered_cost_type = set(crud.get_classified_by_cost_type(cost_type))
    else:
        filtered_cost_type = set(classifieds)

    # Search filter by min and max price
    if request.args.get("price-min"):
        price_min = int(request.args.get("price-min"))
    else:
        price_min = 0
    if request.args.get("price-max"):
        price_max = int(request.args.get("price-max"))
    else:
        price_max = 1000000

    filtered_cost = set(crud.get_classified_by_cost(price_min, price_max))

    # Search filter by haversine miles from zipcode 
    filtered_miles = []
    if request.args.get("miles"):
        input_miles = int(request.args.get("miles"))
    else:
        input_miles = 100000000000000

    if request.args.get("zip"):
        input_zip = int(request.args.get("zip"))
        for classified in classifieds:
            haversine_miles = crud.get_distance_in_miles(input_zip, classified.postal_code)
            if (input_miles >= haversine_miles):
                filtered_miles.append(classified)
    else:
        filtered_miles = classifieds

    search_to_return = list(filtered_cost_type & filtered_tags & filtered_cost & set(classifieds) & set(filtered_miles))

    return render_template('filtered.html', classifieds=search_to_return)
