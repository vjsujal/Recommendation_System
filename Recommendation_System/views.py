from django.shortcuts import render
from recommend import txt_train, image_test, txt_image_test, get_info, get_random, prompt_helper
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
    lst1 = [get_info(i) for i in arr]  # Replace get_info_home with your actual function
    # print(lst1)
    return render(request, 'index.html', {'lst': lst1})

def view_item(request, item_id):
    item = get_info(int(item_id))  # Replace this with your logic to fetch item info
    # Assuming 'product.html' is in a folder named 'templates' within your app directory
    return render(request, 'product.html', {'item_info': item})

@csrf_exempt  # Disable CSRF protection for this view (for demonstration purposes; use CSRF protection in production)
def submit_txt(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            user_text = data.get('message')
            ans = prompt_helper(user_text)
            print(ans)
            if ans['category'] == 1:
                response = {'answer': ans['reply']}
            elif ans['category'] == 2:
                response = {'answer': ans['reply']}
            elif ans['category'] == 3:
                discount = ans['discount']
                product_name = ans['product_name']
                lst = txt_train(product_name)
                # Filter products with discount above the given value
                filtered_lst = [prod for prod in lst if prod[5] > discount]
                # Take the first 5 products from the filtered list
                if len(filtered_lst) < 5:
                    response = {'answer': "Sorry, not much products found with that discount...Try again with a lower discount value."}
                else:
                    response = {
                    f'item{i+1}': filtered_lst[i] for i in range(min(5, len(filtered_lst)))
                }
                return JsonResponse(response)
            else:
                print(ans['suggested_product_name'])
                lst = txt_train(ans['suggested_product_name'])
                response = {
                    'item1': lst[0],
                    'item2': lst[1],
                    'item3': lst[2],
                    'item4': lst[3],
                    'item5': lst[4]
                }
            return JsonResponse(response)
        except Exception as e:
            return JsonResponse({'answer': "Sorry, Unable to process your request. Please try again."})

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

