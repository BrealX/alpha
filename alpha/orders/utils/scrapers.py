def get_areas():
    '''
    Gets Areas list from Delivery-Auto API
    '''
    import django
    django.setup()
    import requests, json
    from orders.models import OrderDeliveryArea, OrderDeliveryCity
    # Sending request for areas
    areas_queryset = OrderDeliveryArea.objects.all()
    errors = []
    url = 'http://www.delivery-auto.com/api/v4/Public/GetRegionList?culture=%s&country=%s' % ('ru-RU', '1')
    headers = {'Content-Type': 'application/json'}
    answer = requests.get(url, headers=headers)
    # Getting responce with data
    data = answer.json()
    # If response code is 200 --> save data
    if answer.status_code == requests.codes.ok:
        if data['status']:
            areas_list = [{'id': area['id'], 'name': area['name']} for area in data['data'][1:]]
            if areas_list:
                for area in areas_list:
                    if not areas_queryset:
                        OrderDeliveryArea.objects.bulk_create([
                            OrderDeliveryArea(
                                name=area['name'], 
                                area_ref=area['id'],
                            )
                        ])
                    else:
                        obj, created = OrderDeliveryArea.objects.get_or_create(name=area['name'])
                        obj.name = area['name']
                        obj.area_ref = area['id']
                        obj.save()
                    return areas_list
        errors.append[data['message']]
        return errors
    return errors


def get_cities():
    '''
    Gets Cities list from Delivery-Auto API
    '''
    import django
    django.setup()
    import requests, json
    from orders.models import OrderDeliveryArea, OrderDeliveryCity
    # Sending request for Cities
    areas_list = OrderDeliveryArea.objects.all() # Get all Areas in database
    for area in areas_list:
        area_ref = area.area_ref # Area reference according to Delivery-Auto codes
        cities_queryset = OrderDeliveryCity.objects.filter(area_id=area.id) # Get all current area Cities in database
        url = 'http://www.delivery-auto.com/api/v4/Public/GetAreasList?culture=%s&regionId=%s&country=%s' % ('ru-RU', area.area_ref, '1') # Delivery-Auto API url
        headers = {'Content-Type': 'application/json'}
        answer = requests.get(url, headers=headers)
        # Getting responce with data
        data = answer.json()
        # If response code is 200 --> save or update data
        if answer.status_code == requests.codes.ok:
            if data['status']: # Checks if any data was received from Delivery-Auto API
                cities_list = [{'id': city['id'], 'name': city['name']} for city in data['data']]
                if cities_list:
                    for city in cities_list:
                        if not cities_queryset: # If there were no objects in OrderDeliveryCity model - create them
                            try:
                                OrderDeliveryCity.objects.bulk_create([
                                    OrderDeliveryCity(
                                        area=OrderDeliveryArea.objects.get(id=area.id),
                                        name=city['name'], 
                                        city_ref=city['id']
                                    )
                                ])
                            except OrderDeliveryArea.DoesNotExist:
                                return errors
                        else: # If there were any objects in OrderDeliveryCity model - update them or create new if needed
                            obj, created = OrderDeliveryCity.objects.get_or_create(name=city['name'])
                            obj.name = city['name']
                            obj.city_ref = city['id']
                            obj.save()
            else:
                print('error, API returned %s' % data['message'])
    print('All job is done')
    return OrderDeliveryCity.objects.all()
