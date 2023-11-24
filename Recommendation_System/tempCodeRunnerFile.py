
def prompt_helper(prompt):
    import google.generativeai as palm
    import os
    palm.configure(api_key="AIzaSyCVeFW87-H5c32e4i0E8KRJ7jgnDOR5lIY")

    pre_prompt = "You are a prompt helper for fashion recomendation system \
    Strictly don't answer questions that are not fashion and fashion accessories related. \
    The chatbot is helpful, creative, clever, and very friendly. \
    Try to get as much information as possible from the user about his issue. \
    Give short answers and don't give very length responses. \
    Don't mention that you are not a fashion recommender specialist as it is already assumed.\
    If user ask that you offer discounts or not you should answer that you offer discounts dont mention the anything about product. \
    If user ask for a recomendation on perticular product or need suggetion of clothes for function then you shoud return the ['user asked pruduct','default'] \
    If user ask for a recomendation on perticular product that is having a price limit then only you shoud return the list of user asked product and 'price' "

    pre_prompt+=f" User: {prompt}"
    response = palm.generate_text(prompt=pre_prompt)
    ans=response.result
    if ans[0]!='[':
        return ans
    return type(eval(response.result))

print(prompt_helper("hello"))