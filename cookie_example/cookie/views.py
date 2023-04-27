from django.shortcuts import render
from .models import *
# Create your views here.
def view_main(request):
    context = {
        "product_list":Product.objects.all()

    }
    response = render(request, "cookie/index.html", context = context)
    # проверка на запрос пост
    if request.method == 'POST':
        # получаем из запроса id продукта 
        id = request.POST.get('go-to-basket')
        # проверка на наличие id-product в файлах COOKIE 
        if 'id-product' in request.COOKIES:
            # записываем старые COOKIE в переменную 
            old_cookie = request.COOKIES['id-product']
            #Проверка на наличие товара в COOKIE файлах
            if id not in old_cookie:
                #Создание строки с новыми товарами и с учётом старых 
                new_cookie = id + " " + old_cookie
                #Создание COOKIE сновыми товарами
                response.set_cookie('id-product', new_cookie)
        else:
            #Если продуктов нет в запросе, создание нового COOKIE 
            response.set_cookie('id-product', id)
    #Возвращение ответа    
    return response

    

def view_basket(request):
    # проверка наличия добавленых продуктов в куки
    if "id-product" in request.COOKIES:

        # передача куки в переменую id
        id = request.COOKIES["id-product"]  
        # розсоединение айдишек елементов через пробел и передача их в список
        list = id.split(" ")

        if request.method == 'POST':
            
            id_del = request.POST.get('go-into-basket')
            list.remove(id_del)
            new_cookie = ''
            for cookie in list:
                new_cookie += cookie 
    else:
        # если продуктов нет в куки, то и список переданых продуктов будет пустым
        list = []
        
    if len(list) != 0:
        list.pop(len(list)-1)
    
    # контекст
    context = {
        "product_list": Product.objects.filter(pk__in = list) # фильтруем продукты для вывода их в basket, по их наличию в списке
    }
    # создание ответа
    response = render(request, "cookie/basket.html", context=context)

    if request.method == 'POST':
        if "id-product" in request.COOKIES:
            response.set_cookie('id-product', new_cookie)
         

    # отправка ответа 
    return response

