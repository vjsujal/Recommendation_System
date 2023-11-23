from django.shortcuts import render
from recommend import txt_train, image_test, txt_image_test, get_info, get_random, get_info_home
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
from django.conf import settings

# upload_folder = os.path.join(settings.BASE_DIR, 'uploads')
upload_folder = settings.UPLOAD_FOLDER

if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)

def home(request):
    arr = get_random()  # Replace with your logic to get random values
    lst1 = [get_info_home(i) for i in arr]  # Replace get_info_home with your actual function
    # print(lst1)
    return render(request, 'index.html', {'lst': lst1})

def view_item(request, item_id):
    item = get_info(int(item_id))  # Replace this with your logic to fetch item info
    # Assuming 'product.html' is in a folder named 'templates' within your app directory
    return render(request, 'product.html', {'item_info': item})

@csrf_exempt  # Disable CSRF protection for this view (for demonstration purposes; use CSRF protection in production)
def submit_txt(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        user_text = data.get('message')
        lst = txt_train(user_text)  # Assuming txt_train is a function defined somewhere

        response = {
            'item1': lst[0],
            'item2': lst[1],
            'item3': lst[2],
            'item4': lst[3],
            'item5': lst[4]
        }

        return JsonResponse(response)

    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt  # Disable CSRF protection for this view (for demonstration purposes; use CSRF protection in production)
def submit_img(request):
    if request.method == 'POST' and 'image' in request.FILES:
        uploaded_file = request.FILES['image']
        
        if uploaded_file.name != '':
            image_path = os.path.join(upload_folder, uploaded_file.name)
            with open(image_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
            
            lst = image_test(image_path)  # Assuming image_test is a function defined somewhere
            os.remove(image_path)
            
            response = {
                'item1': lst[0],
                'item2': lst[1],
                'item3': lst[2],
                'item4': lst[3],
                'item5': lst[4]
            }
            return JsonResponse(response)
    
    return JsonResponse({'error': 'Image upload failed'}, status=400)


@csrf_exempt  # Disable CSRF protection for this view (for demonstration purposes; use CSRF protection in production)
def submit_both(request):
    if request.method == 'POST' and 'image' in request.FILES and 'message' in request.POST:
        uploaded_file = request.FILES['image']
        user_text = request.POST.get('message')
        
        if uploaded_file.name != '':
            image_path = os.path.join(upload_folder, uploaded_file.name)
            with open(image_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
            
            lst = txt_image_test(user_text, image_path)  # Assuming txt_image_test is a function defined somewhere
            os.remove(image_path)
            
            response = {
                'item1': lst[0],
                'item2': lst[1],
                'item3': lst[2],
                'item4': lst[3],
                'item5': lst[4]
            }
            return JsonResponse(response)
    
    return JsonResponse({'error': 'Image or text submission failed'}, status=400)